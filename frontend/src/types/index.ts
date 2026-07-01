export interface Transaction {
  id: string;
  amount: number;
  description: string;
  category: string;
  type: "income" | "expense";
  date: string;
  account_id: string;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface Account {
  id: string;
  name: string;
  type: "checking" | "savings" | "credit" | "cash" | "investment";
  balance: number;
  currency: string;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface Budget {
  id: string;
  category: string;
  limit: number;
  spent: number;
  period: "monthly" | "weekly" | "yearly";
  start_date: string;
  user_id: string;
}

export interface FinancialProfile {
  id: string;
  user_id: string;
  currency: string;
  salary_day: number;
  onboarding_complete: boolean;
  created_at: string;
  updated_at: string;
}

export interface IncomeSource {
  id: string;
  user_id: string;
  name: string;
  amount: number;
  type: "salary" | "freelance" | "investment" | "other";
  created_at: string;
  updated_at: string;
}

export interface FixedExpense {
  id: string;
  user_id: string;
  name: string;
  amount: number;
  category: string;
  created_at: string;
  updated_at: string;
}

export interface Debt {
  id: string;
  user_id: string;
  name: string;
  total_amount: number;
  remaining_amount: number;
  interest_rate: number;
  payment_per_month: number;
  start_date: string;
  created_at: string;
  updated_at: string;
}

export interface FinancialGoal {
  id: string;
  user_id: string;
  name: string;
  target_amount: number;
  saved_amount: number;
  deadline: string;
  category: string;
  created_at: string;
  updated_at: string;
}

export interface DashboardStats {
  total_balance: number;
  monthly_income: number;
  monthly_expenses: number;
  total_debt: number;
  savings_rate: number;
  num_accounts: number;
  num_transactions: number;
}
