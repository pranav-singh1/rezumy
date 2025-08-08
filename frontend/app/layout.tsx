export const metadata = {
  title: 'Rezumy',
  description: 'Agentic job application assistant'
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
} 