import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "LGTM Bot - AI-Powered Code Review",
  description: "Automate code reviews with AI. Connect Jira tickets to GitHub PRs for intelligent, comprehensive code analysis that saves time and improves quality.",
  keywords: "code review, AI, GitHub, Jira, automation, pull request, code quality",
  authors: [{ name: "LGTM Bot Team" }],
  openGraph: {
    title: "LGTM Bot - AI-Powered Code Review",
    description: "Automate code reviews with AI. Connect Jira tickets to GitHub PRs for intelligent analysis.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
        suppressHydrationWarning={true}
      >
        {children}
      </body>
    </html>
  );
}