"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@clerk/nextjs";
import { Wallet, Banknote, Check, ArrowRight, ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const STEPS = [
  { id: 1, title: "Income", icon: Banknote },
  { id: 2, title: "Fixed Expenses", icon: Wallet },
  { id: 3, title: "Done", icon: Check },
];

interface IncomeData {
  amount: string;
  name: string;
}

interface FixedExpenseData {
  name: string;
  amount: string;
  category: string;
}

export function OnboardingWizard() {
  const router = useRouter();
  const { getToken } = useAuth();
  const [currentStep, setCurrentStep] = useState(1);
  const [loading, setLoading] = useState(false);

  // Income state
  const [income, setIncome] = useState<IncomeData>({
    amount: "",
    name: "Monthly Salary",
  });

  // Fixed expenses state
  const [expenses, setExpenses] = useState<FixedExpenseData[]>([
    { name: "Rent", amount: "", category: "housing" },
    { name: "Food", amount: "", category: "food" },
    { name: "Transport", amount: "", category: "transport" },
    { name: "Bills", amount: "", category: "bills" },
    { name: "Subscriptions", amount: "", category: "subscriptions" },
  ]);

  const addExpense = () => {
    setExpenses([
      ...expenses,
      { name: "", amount: "", category: "other" },
    ]);
  };

  const removeExpense = (index: number) => {
    setExpenses(expenses.filter((_, i) => i !== index));
  };

  const updateExpense = (
    index: number,
    field: keyof FixedExpenseData,
    value: string
  ) => {
    const updated = [...expenses];
    updated[index] = { ...updated[index], [field]: value };
    setExpenses(updated);
  };

  const totalFixedExpenses = expenses.reduce(
    (sum, e) => sum + (parseFloat(e.amount) || 0),
    0
  );

  const handleComplete = async () => {
    setLoading(true);
    try {
      const token = await getToken();

      // 1. Create financial profile
      await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/profile`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          currency: "THB",
          salary_day: 18,
        }),
      });

      // 2. Create income source
      await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/income`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          name: income.name || "Monthly Salary",
          amount: parseFloat(income.amount) || 0,
          type: "salary",
        }),
      });

      // 3. Create fixed expenses
      for (const expense of expenses) {
        if (expense.name && expense.amount) {
          await fetch(
            `${process.env.NEXT_PUBLIC_API_URL}/api/v1/fixed-expenses`,
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
              },
              body: JSON.stringify({
                name: expense.name,
                amount: parseFloat(expense.amount),
                category: expense.category,
              }),
            }
          );
        }
      }

      // 4. Mark onboarding complete
      await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/profile/complete-onboarding`,
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );

      router.push("/dashboard");
    } catch (error) {
      console.error("Onboarding failed:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <Card className="w-full max-w-xl">
        <CardHeader className="text-center">
          <div className="flex items-center justify-center gap-2 mb-2">
            <Wallet className="h-8 w-8 text-primary" />
            <span className="text-2xl font-bold">Money OS</span>
          </div>
          <CardTitle>Let&apos;s set up your finances</CardTitle>
          <CardDescription>
            Tell us about your income and expenses so we can help you manage
            your money.
          </CardDescription>

          {/* Step indicator */}
          <div className="flex items-center justify-center gap-2 mt-6">
            {STEPS.map((step, i) => (
              <div key={step.id} className="flex items-center gap-2">
                <div
                  className={`flex h-8 w-8 items-center justify-center rounded-full text-sm font-medium transition-colors ${
                    currentStep >= step.id
                      ? "bg-primary text-primary-foreground"
                      : "bg-muted text-muted-foreground"
                  }`}
                >
                  {currentStep > step.id ? (
                    <Check className="h-4 w-4" />
                  ) : (
                    step.id
                  )}
                </div>
                {i < STEPS.length - 1 && (
                  <div
                    className={`h-0.5 w-12 transition-colors ${
                      currentStep > step.id
                        ? "bg-primary"
                        : "bg-muted"
                    }`}
                  />
                )}
              </div>
            ))}
          </div>
        </CardHeader>

        <CardContent>
          {/* Step 1: Income */}
          {currentStep === 1 && (
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold flex items-center gap-2">
                  <Banknote className="h-5 w-5" />
                  What&apos;s your monthly income?
                </h3>
                <p className="text-sm text-muted-foreground mt-1">
                  Enter your primary income source
                </p>
              </div>

              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="income-name">Income Name</Label>
                  <Input
                    id="income-name"
                    placeholder="e.g., Monthly Salary"
                    value={income.name}
                    onChange={(e) =>
                      setIncome({ ...income, name: e.target.value })
                    }
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="income-amount">Amount (THB)</Label>
                  <Input
                    id="income-amount"
                    type="number"
                    placeholder="e.g., 35000"
                    value={income.amount}
                    onChange={(e) =>
                      setIncome({ ...income, amount: e.target.value })
                    }
                  />
                </div>
              </div>

              <div className="flex justify-end">
                <Button onClick={() => setCurrentStep(2)}>
                  Next
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </div>
            </div>
          )}

          {/* Step 2: Fixed Expenses */}
          {currentStep === 2 && (
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold flex items-center gap-2">
                  <Wallet className="h-5 w-5" />
                  What are your fixed expenses?
                </h3>
                <p className="text-sm text-muted-foreground mt-1">
                  Add your recurring monthly costs
                </p>
              </div>

              <div className="space-y-3">
                {expenses.map((expense, index) => (
                  <div
                    key={index}
                    className="flex items-center gap-3 p-3 rounded-lg border bg-background"
                  >
                    <div className="flex-1 grid grid-cols-[1fr_100px] gap-2">
                      <Input
                        placeholder="Expense name"
                        value={expense.name}
                        onChange={(e) =>
                          updateExpense(index, "name", e.target.value)
                        }
                      />
                      <Input
                        type="number"
                        placeholder="0"
                        value={expense.amount}
                        onChange={(e) =>
                          updateExpense(index, "amount", e.target.value)
                        }
                      />
                    </div>
                    <Badge variant="secondary" className="text-xs">
                      {expense.category}
                    </Badge>
                    {expenses.length > 1 && (
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => removeExpense(index)}
                        className="text-destructive"
                      >
                        ✕
                      </Button>
                    )}
                  </div>
                ))}

                <Button
                  variant="outline"
                  onClick={addExpense}
                  className="w-full border-dashed"
                >
                  + Add Expense
                </Button>
              </div>

              <div className="flex items-center justify-between p-3 rounded-lg bg-muted">
                <span className="text-sm font-medium">Total Fixed Expenses</span>
                <span className="text-lg font-bold">
                  {totalFixedExpenses.toLocaleString()} THB
                </span>
              </div>

              <div className="flex justify-between">
                <Button variant="outline" onClick={() => setCurrentStep(1)}>
                  <ArrowLeft className="mr-2 h-4 w-4" />
                  Back
                </Button>
                <Button onClick={() => setCurrentStep(3)}>
                  Next
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </div>
            </div>
          )}

          {/* Step 3: Summary */}
          {currentStep === 3 && (
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold flex items-center gap-2">
                  <Check className="h-5 w-5" />
                  All done! Here&apos;s your summary
                </h3>
              </div>

              <div className="space-y-3">
                <div className="flex items-center justify-between p-3 rounded-lg border">
                  <span className="text-sm">Monthly Income</span>
                  <Badge variant="default" className="text-sm px-3 py-1">
                    + {parseFloat(income.amount || "0").toLocaleString()} THB
                  </Badge>
                </div>
                <div className="flex items-center justify-between p-3 rounded-lg border">
                  <span className="text-sm">Fixed Expenses</span>
                  <Badge variant="destructive" className="text-sm px-3 py-1">
                    - {totalFixedExpenses.toLocaleString()} THB
                  </Badge>
                </div>
                <div className="flex items-center justify-between p-3 rounded-lg border bg-primary/5">
                  <span className="text-sm font-medium">
                    Remaining (for savings & goals)
                  </span>
                  <Badge
                    variant="default"
                    className="text-sm px-3 py-1 bg-emerald-600"
                  >
                    {(
                      (parseFloat(income.amount || "0") || 0) - totalFixedExpenses
                    ).toLocaleString()}{" "}
                    THB
                  </Badge>
                </div>
              </div>

              <div className="flex justify-between">
                <Button variant="outline" onClick={() => setCurrentStep(2)}>
                  <ArrowLeft className="mr-2 h-4 w-4" />
                  Back
                </Button>
                <Button onClick={handleComplete} disabled={loading}>
                  {loading ? "Saving..." : "Start Managing Money"}
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
