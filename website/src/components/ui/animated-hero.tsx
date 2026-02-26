"use client";

import { useEffect, useMemo, useState } from "react";
import { motion } from "framer-motion";
import { MoveRight } from "lucide-react";
import { HoverBorderGradient } from "@/components/ui/hover-border-gradient";

function Hero() {
  const [titleNumber, setTitleNumber] = useState(0);
  const titles = useMemo(
    () => ["smarter", "faster", "AI-driven", "secure", "streamlined"],
    []
  );

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      if (titleNumber === titles.length - 1) {
        setTitleNumber(0);
      } else {
        setTitleNumber(titleNumber + 1);
      }
    }, 2000);
    return () => clearTimeout(timeoutId);
  }, [titleNumber, titles]);

  return (
    <div className="w-full relative">
      {/* Enhanced radial gradient background with more visible blue tones */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,rgba(59,130,246,0.1)_0%,rgba(59,130,246,0.05)_50%,transparent_70%)] dark:bg-[radial-gradient(ellipse_at_center,rgba(59,130,246,0.15)_0%,rgba(59,130,246,0.08)_50%,transparent_70%)] pointer-events-none"></div>
      
      <div className="container mx-auto relative z-10">
        <div className="flex gap-8 py-24 lg:py-40 items-center justify-center flex-col">
          <div>
            <HoverBorderGradient className="gap-4">
              <div className="flex items-center">
                AI-Powered Code Review <MoveRight className="w-5 h-5 ml-2" />
              </div>
            </HoverBorderGradient>
          </div>
          <div className="flex gap-4 flex-col">
            <h1 className="text-6xl md:text-8xl max-w-2xl tracking-tighter text-center font-regular">
              <span className="text-spektr-cyan-50">Automated PR Reviews,</span>
              <span className="relative flex w-full justify-center overflow-hidden text-center md:pb-4 md:pt-1">
                &nbsp;
                {titles.map((title, index) => (
                  <motion.span
                    key={index}
                    className="absolute font-semibold"
                    initial={{ opacity: 0, y: "-100" }}
                    transition={{ type: "spring", stiffness: 50 }}
                    animate={
                      titleNumber === index
                        ? {
                            y: 0,
                            opacity: 1,
                          }
                        : {
                            y: titleNumber > index ? -150 : 150,
                            opacity: 0,
                          }
                    }
                  >
                    {title}
                  </motion.span>
                ))}
              </span>
            </h1>

            <p className="text-lg md:text-xl leading-relaxed tracking-tight text-muted-foreground max-w-2xl text-center">
              LGTM Bot connects GitHub and Jira to provide AI-powered reviews, objective scoring, and actionable feedback on every pull request. Boost code quality and ship with confidence locally or in CI/CD.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export { Hero };
