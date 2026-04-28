import "./globals.css";

export const metadata = {
  title: "TRADEXBOT Dashboard",
  description: "Control panel for automated trading bot"
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
