import type { Metadata } from "next";
import "./globals.css";
import { Providers } from "@/components/Providers"
import Navbar from "@/components/layout/Navbar"



export const metadata: Metadata = {
  title: "Pizza Con",
  description: "",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <Providers>
          <Navbar />
          <main className="min-h-screen bg-background">
            {children}
          </main>
        </Providers>
      </body>
    </html>
  );
}
