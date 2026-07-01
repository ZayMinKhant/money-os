"use client";

import { useAuth, useUser } from "@clerk/nextjs";
import { useEffect, useState } from "react";
import { redirect } from "next/navigation";
import { Plus, Landmark, Target, FileText } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import type { DashboardStats } from "@/types";

export default function DashboardPage() {
  const { getToken } = useAuth();
  const { user } = useUser();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  const firstName = user?.firstName || "User";

  useEffect(() => {
    async function fetchData() {
      const token = await getToken();
      if (!token) return;

      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

      try {
        // Check if onboarding is complete
        const profileRes = await fetch(`${apiUrl}/api/v1/profile`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (profileRes.status === 404) {
          redirect("/onboarding");
          return;
        }

        const profileData = await profileRes.json();
        if (!profileData.onboarding_complete) {
          redirect("/onboarding");
          return;
        }

        // Fetch dashboard stats
        const statsRes = await fetch(`${apiUrl}/api/v1/dashboard/stats`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (statsRes.ok) {
          const statsData = await statsRes.json();
          setStats(statsData);
        }
      } catch (error) {
        console.error("Failed to fetch dashboard data:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [getToken]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-pulse text-muted-foreground">Loading...</div>
      </div>
    );
  }

  const formatTHB = (amount: number) =>
    `${amount.toLocaleString("en-US", { minimumFractionDigits: 2 })} THB`;

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight">
          Welcome back, {firstName}
        </h1>
        <p className="text-muted-foreground">
          Here&apos;s an overview of your financial health.
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-5">
        <StatsCard
          title="Total Balance"
          value={stats ? formatTHB(stats.total_balance) : "0.00 THB"}
          description="Across all accounts"
        />
        <StatsCard
          title="Monthly Income"
          value={stats ? formatTHB(stats.monthly_income) : "0.00 THB"}
          description="This month"
        />
        <StatsCard
          title="Monthly Expenses"
          value={stats ? formatTHB(stats.monthly_expenses) : "0.00 THB"}
          description="This month"
        />
        <StatsCard
          title="Total Debt"
          value={stats ? formatTHB(stats.total_debt) : "0.00 THB"}
          description="Remaining"
        />
        <StatsCard
          title="Savings Rate"
          value={stats ? `${stats.savings_rate}%` : "0%"}
          description="Target: 20%"
        />
      </div>

      {/* Content Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        {/* Recent Transactions */}
        <div className="col-span-full lg:col-span-4">
          <div className="rounded-xl border bg-card p-6">
            <h3 className="text-lg font-semibold">Recent Transactions</h3>
            <p className="text-sm text-muted-foreground mb-4">
              Your latest financial activity
            </p>
            <div className="space-y-3">
              {[1, 2, 3].map((i) => (
                <div
                  key={i}
                  className="flex items-center justify-between rounded-lg border p-3"
                >
                  <div className="space-y-1">
                    <p className="text-sm font-medium">No transactions yet</p>
                    <p className="text-xs text-muted-foreground">
                      Add your first transaction to get started
                    </p>
                  </div>
                  <Badge variant="secondary">Empty</Badge>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="col-span-full lg:col-span-3">
          <div className="rounded-xl border bg-card p-6">
            <h3 className="text-lg font-semibold">Quick Actions</h3>
            <p className="text-sm text-muted-foreground mb-4">
              Manage your finances
            </p>
            <div className="grid gap-3">
              <Button variant="outline" className="justify-start h-auto py-3">
                <Plus className="mr-2 h-4 w-4" />
                Add Transaction
              </Button>
              <Button variant="outline" className="justify-start h-auto py-3">
                <Landmark className="mr-2 h-4 w-4" />
                Add Account
              </Button>
              <Button variant="outline" className="justify-start h-auto py-3">
                <Target className="mr-2 h-4 w-4" />
                Set Budget
              </Button>
              <Button variant="outline" className="justify-start h-auto py-3">
                <FileText className="mr-2 h-4 w-4" />
                View Reports
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function StatsCard({
  title,
  value,
  description,
}: {
  title: string;
  value: string;
  description: string;
}) {
  return (
    <div className="rounded-xl border bg-card p-6">
      <div className="flex flex-col space-y-1">
        <p className="text-sm font-medium text-muted-foreground">{title}</p>
        <p className="text-2xl font-bold">{value}</p>
        <p className="text-xs text-muted-foreground">{description}</p>
      </div>
    </div>
  );
}
