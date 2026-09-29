import "./globals.css";

export const metadata = {
  title: "AI Research Analyst",
  description: "Evidence-grounded research using RAG and local LLMs",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}