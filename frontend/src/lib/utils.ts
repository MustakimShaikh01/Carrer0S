/**
 * Utility function for merging class names (Tailwind-friendly).
 */
import { type ClassValue, clsx } from "clsx";

export function cn(...inputs: ClassValue[]) {
  return clsx(inputs);
}
