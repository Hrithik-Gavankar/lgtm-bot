import { Hero } from "@/components/ui/animated-hero";
import { Header } from "@/components/ui/header";
import { Features } from "@/components/ui/features";


export default function Home() {
  return (
    <div className="min-h-screen bg-white dark:bg-black">

      {/* Animated Hero Section */}
      <Hero />
      <Header />
      <Features />
     
    </div>
  );
}
