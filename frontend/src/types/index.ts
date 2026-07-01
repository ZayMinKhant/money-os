export interface Transaction {
  id: string;
  amount: number;
  description: string;
  category: string;
  type: "income" | "expense";
  date: string;
  created_at: string;
}

export interface Account {
  id: string;
  name: string;
  type: "checking" | "savings" | "credit" | "cash" | "investment";
  balance: number;
  currency: string;
  created_at: string;
}

export interface Budget {
  id: string;
  category: string;
  limit: number;
  spent: number;
  period: "monthly" | "weekly" | "yearly";
  start_date: string;
}

export interface DashboardStats {
  totalBalance: number;
  totalIncome: number;
  totalExpenses: number;
  savingsRate: number;
  recentTransactions: Transaction[];
}
