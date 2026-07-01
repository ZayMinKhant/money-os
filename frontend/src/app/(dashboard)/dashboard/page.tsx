import { currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import { Plus, Landmark, Target, FileText } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export default async function DashboardPage() {
  const user = await currentUser();

  if (!user) {
    redirect("/sign-in");
  }

  const firstName = user.firstName || "User";

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
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatsCard
          title="Total Balance"
          value="$0.00"
          description="Across all accounts"
          trend="neutral"
        />
        <StatsCard
          title="Monthly Income"
          value="$0.00"
          description="This month"
          trend="up"
        />
        <StatsCard
          title="Monthly Expenses"
          value="$0.00"
          description="This month"
          trend="down"
        />
        <StatsCard
          title="Savings Rate"
          value="0%"
          description="Target: 20%"
          trend="neutral"
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
                      Connect your accounts to get started
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
              Get started with Money OS
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
  trend,
}: {
  title: string;
  value: string;
  description: string;
  trend: "up" | "down" | "neutral";
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
