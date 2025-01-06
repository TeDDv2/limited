import express, { Request, Response } from 'express';
import { Pool } from 'pg';
import { createClient } from 'redis';
import http from 'http';
import { Server } from 'socket.io';
import path from 'path';
import cors from "cors";
import NodeCache from 'node-cache';
import { promisify } from 'util';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: process.env.CORS_ORIGIN || "*",
    methods: ["GET", "POST"]
  }
});

const pool = new Pool({
  user: process.env.DB_USER,
  host: process.env.DB_HOST,
  database: process.env.DB_NAME,
  password: process.env.DB_PASSWORD,
  port: parseInt(process.env.DB_PORT || '5432'),
});

const redisClient = createClient({
  url: process.env.REDIS_URL
});

(async () => {
  await redisClient.connect();
})();

const appCache = new NodeCache({ stdTTL: 100, checkperiod: 120 });

app.use(cors());
app.use(express.json());

const getProductData = async () => {
  const cachedData = appCache.get('productData');
  if (cachedData) return cachedData;

  const productsQuery = await pool.query('SELECT * FROM products');
  const sizesQuery = await pool.query('SELECT * FROM sizes');
  const data = {
    products: productsQuery.rows,
    sizes: sizesQuery.rows,
  };

  await redisClient.set('productData', JSON.stringify(data));
  appCache.set('productData', data);

  return data;
};

app.get("/", async(req: Request, res: Response) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.post('/update-price', async (req: Request, res: Response) => {
  const { pid } = req.body;
  try {
    const result = await pool.query('UPDATE products SET updated_price = FALSE WHERE pid = $1 RETURNING updated_price', [pid]);
    const updatedData = await getProductData();
    io.emit('update', updatedData);
    res.json({ success: true, updatedPrice: result.rows[0].updated_price });
  } catch (err) {
    console.error(err);
    res.status(500).json({ success: false, error: 'Server error' });
  }
});

app.post('/update-size', async (req: Request, res: Response) => {
  const { pid, sizeName } = req.body;
  try {
    const result = await pool.query('UPDATE sizes SET updated_size = FALSE WHERE pid = $1 AND name = $2 RETURNING updated_size', [pid, sizeName]);
    const updatedData = await getProductData();
    io.emit('update', updatedData);
    res.json({ success: true, updatedSize: result.rows[0].updated_size });
  } catch (err) {
    console.error(err);
    res.status(500).json({ success: false, error: 'Server error' });
  }
});

app.get('/products', async (req: Request, res: Response) => {
  try {
    const data = await getProductData();
    res.json(data);
  } catch (err) {
    console.error(err);
    res.status(500).send('Server error');
  }
});

const listenForChanges = async () => {
  const client = await pool.connect();
  try {
    await client.query('LISTEN product_update');
    client.on('notification', async (msg) => {
      if (msg.channel === 'product_update') {
        const updatedData = await getProductData();
        io.emit('update', updatedData);
      }
    });
  } catch (error) {
    console.error('Error in listenForChanges:', error);
  }
};

listenForChanges();

io.on('connection', (socket) => {
  console.log('A user connected');
  socket.emit('connected', 'You are connected to the server');
});

const PORT = process.env.PORT || 3700;
server.listen(PORT, () => {
  console.log(`Server běží na http://localhost:${PORT}`);
});