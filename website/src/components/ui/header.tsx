"use client";

import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu";
import { Menu, X, Code, Github } from "lucide-react";
import { useState } from "react";
import Link from "next/link";

type NavigationItem = {
  name: string;
  href?: string;
  description?: string;
  items?: NavigationItem[];
};

function Header() {
  const [isOpen, setOpen] = useState(false);

  const navigationItems: NavigationItem[] = [
    {
      name: 'Features',
      href: '#features',
      description: 'Discover powerful features of LGTM Bot for code reviews'
    },
  ];

  return (
    // --- Made the header more transparent ---
    <header className="fixed top-0 left-0 right-0 z-50 bg-white/30 dark:bg-black/30 backdrop-blur-xl border-b border-white/10 dark:border-black/10">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex min-h-16 items-center justify-between">
          {/* Logo */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-black dark:bg-white rounded-lg flex items-center justify-center">
                <Code className="w-5 h-5 text-white dark:text-black" />
              </div>
              <span className="text-xl font-bold text-black dark:text-white">LGTM Bot</span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-1">
            <NavigationMenu>
              <NavigationMenuList>
                {navigationItems.map((item) => (
                  <NavigationMenuItem key={item.name}>
                    {item.items ? (
                      <>
                        <NavigationMenuTrigger className="bg-transparent hover:bg-black/5 dark:hover:bg-white/10 data-[state=open]:bg-black/5 dark:data-[state=open]:bg-white/10 text-black dark:text-white">
                          {item.name}
                        </NavigationMenuTrigger>
                        <NavigationMenuContent>
                          <ul className="grid w-[400px] gap-3 p-4 md:w-[500px] md:grid-cols-2 lg:w-[600px]">
                            {item.items.map((subItem) => (
                              <li key={subItem.name}>
                                <NavigationMenuLink asChild>
                                  <Link
                                    href={subItem.href!}
                                    className="block select-none space-y-1 rounded-md p-3 leading-none no-underline outline-none transition-colors hover:bg-black/5 dark:hover:bg-white/10"
                                  >
                                    <div className="text-sm font-medium leading-none text-black dark:text-white">
                                      {subItem.name}
                                    </div>
                                    <p className="line-clamp-2 text-sm leading-snug text-black/60 dark:text-white/60">
                                      {subItem.description}
                                    </p>
                                  </Link>
                                </NavigationMenuLink>
                              </li>
                            ))}
                          </ul>
                        </NavigationMenuContent>
                      </>
                    ) : (
                      <NavigationMenuLink asChild>
                        <Link href={item.href!} className={navigationMenuTriggerStyle()}>
                          {item.name}
                        </Link>
                      </NavigationMenuLink>
                    )}
                  </NavigationMenuItem>
                ))}
              </NavigationMenuList>
            </NavigationMenu>

            <div className="ml-4 flex items-center space-x-2">
              <a
                href="https://github.com/Hrithik-Gavankar/lgtm-bot"
                target="_blank"
                rel="noopener noreferrer"
                className="p-2 text-black/70 hover:text-black dark:text-white/70 dark:hover:text-white transition-colors"
              >
                <Github className="h-5 w-5" />
              </a>
            </div>
          </nav>

          {/* Mobile menu button */}
          <div className="flex md:hidden">
            <button
              onClick={() => setOpen(!isOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md text-black dark:text-white hover:bg-black/5 dark:hover:bg-white/10 focus:outline-none"
              aria-label="Toggle menu"
            >
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {isOpen && (
        // --- Made the mobile menu more transparent ---
        <div className="md:hidden bg-white/30 dark:bg-black/30 backdrop-blur-xl border-t border-white/10 dark:border-black/10">
          <div className="px-2 pt-2 pb-3 space-y-1">
            {navigationItems.map((item) => (
              <div key={item.name} className="px-3 py-2">
                {item.items ? (
                  <div>
                    <div className="text-black dark:text-white font-medium px-3 py-2">
                      {item.name}
                    </div>
                    <div className="mt-1 space-y-1 pl-4">
                      {item.items.map((subItem) => (
                        <Link
                          key={subItem.name}
                          href={subItem.href!}
                          className="block px-3 py-2 text-black/70 hover:bg-black/5 dark:text-white/70 dark:hover:bg-white/10 rounded-md"
                          onClick={() => setOpen(false)}
                        >
                          <div className="font-medium">{subItem.name}</div>
                          <p className="text-sm text-black/60 dark:text-white/60">
                            {subItem.description}
                          </p>
                        </Link>
                      ))}
                    </div>
                  </div>
                ) : (
                  <Link
                    href={item.href!}
                    className="block px-3 py-2 text-black/70 hover:bg-black/5 dark:text-white/70 dark:hover:bg-white/10 rounded-md"
                    onClick={() => setOpen(false)}
                  >
                    <div className="font-medium">{item.name}</div>
                    {item.description && (
                      <p className="text-sm text-black/60 dark:text-white/60">
                        {item.description}
                      </p>
                    )}
                  </Link>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </header>
  );
}

export { Header };

