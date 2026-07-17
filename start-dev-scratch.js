import { dev } from 'astro';

try {
  console.log('Starting Astro dev server programmatically...');
  const server = await dev({
    root: '.',
    server: {
      port: 4321,
      host: true
    }
  });
  console.log('Astro dev server started successfully.');
} catch (err) {
  console.error('Error starting Astro dev server:', err);
}
