export interface Product {
  id: number;
  name: string;
  quantity: number;
  unit: string;
}

export type ProductData = Omit<Product, "id">;

export interface Recipe {
  id: number;
  name: string;
  description: string;
}

type Column = {
  id: string;
  label: string;
};

type Row<T extends any> = Record<T, string>;
