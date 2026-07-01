"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Receipt,
  Landmark,
  Target,
  BarChart3,
  Settings,
  Wallet,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";

const navItems = [
  { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { label: "Transactions", href: "/dashboard/transactions", icon: Receipt },
  { label: "Accounts", href: "/dashboard/accounts", icon: Landmark },
  { label: "Budgets", href: "/dashboard/budgets", icon: Target },
  { label: "Reports", href: "/dashboard/reports", icon: BarChart3 },
];

const bottomNavItems = [
  { label: "Settings", href: "/dashboard/settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden md:flex w-64 flex-col border-r bg-card">
      {/* Logo */}
      <div className="flex h-16 items-center gap-2 px-6">
        <Wallet className="h-6 w-6 text-primary" />
        <span className="text-lg font-bold">Money OS</span>
      </div>

      <Separator />

      {/* Navigation */}
      <nav className="flex-1 space-y-1 px-3 py-4">
        {navItems.map((item) => (
          <Link key={item.href} href={item.href}>
            <Button
              variant={pathname === item.href ? "secondary" : "ghost"}
              className={cn(
                "w-full justify-start gap-3",
                pathname === item.href && "bg-secondary"
              )}
            >
              <item.icon className="h-4 w-4" />
              {item.label}
            </Button>
          </Link>
        ))}
      </nav>

      {/* Bottom Nav */}
      <div className="space-y-1 px-3 py-4 border-t">
        {bottomNavItems.map((item) => (
          <Link key={item.href} href={item.href}>
            <Button
              variant="ghost"
              className="w-full justify-start gap-3"
            >
              <item.icon className="h-4 w-4" />
              {item.label}
            </Button>
          </Link>
        ))}
      </div>
    </aside>
  );
}
