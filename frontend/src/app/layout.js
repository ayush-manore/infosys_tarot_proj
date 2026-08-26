import './globals.css';

export const metadata = {
  title: 'MysticAI — Palmistry & Tarot Intelligence Platform',
  description: 'AI-powered spiritual intelligence platform analyzing palm images and tarot cards for personalized life guidance.',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="dark">
      <body className="bg-cosmic-950 text-gray-100 min-h-screen flex flex-col antialiased selection:bg-purple-500 selection:text-white">
        {children}
      </body>
    </html>
  );
}
