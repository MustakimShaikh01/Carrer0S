/**
 * API client for the CareerOS FastAPI backend.
 *
 * Handles JWT auth, token refresh, and typed API responses.
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

interface TokenPair {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

interface ApiError {
  error: {
    code: string;
    message: string;
  };
}

class ApiClient {
  private accessToken: string | null = null;
  private refreshToken: string | null = null;

  constructor() {
    if (typeof window !== "undefined") {
      this.accessToken = localStorage.getItem("careeros_access_token");
      this.refreshToken = localStorage.getItem("careeros_refresh_token");
    }
  }

  // ── Auth state ──────────────────────────────────────────────────────
  setTokens(tokens: TokenPair) {
    this.accessToken = tokens.access_token;
    this.refreshToken = tokens.refresh_token;
    if (typeof window !== "undefined") {
      localStorage.setItem("careeros_access_token", tokens.access_token);
      localStorage.setItem("careeros_refresh_token", tokens.refresh_token);
    }
  }

  clearTokens() {
    this.accessToken = null;
    this.refreshToken = null;
    if (typeof window !== "undefined") {
      localStorage.removeItem("careeros_access_token");
      localStorage.removeItem("careeros_refresh_token");
    }
  }

  get isAuthenticated(): boolean {
    return !!this.accessToken;
  }

  // ── Core fetch ──────────────────────────────────────────────────────
  private async request<T>(
    path: string,
    options: RequestInit = {}
  ): Promise<T> {
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      ...(options.headers as Record<string, string>),
    };

    if (this.accessToken) {
      headers["Authorization"] = `Bearer ${this.accessToken}`;
    }

    const response = await fetch(`${API_BASE}${path}`, {
      ...options,
      headers,
    });

    // Attempt token refresh on 401
    if (response.status === 401 && this.refreshToken) {
      const refreshed = await this.tryRefresh();
      if (refreshed) {
        headers["Authorization"] = `Bearer ${this.accessToken}`;
        const retryResponse = await fetch(`${API_BASE}${path}`, {
          ...options,
          headers,
        });
        if (!retryResponse.ok) {
          throw await this.parseError(retryResponse);
        }
        return retryResponse.json();
      }
      // Refresh failed — clear tokens
      this.clearTokens();
      if (typeof window !== "undefined") {
        window.location.href = "/login";
      }
    }

    if (!response.ok) {
      throw await this.parseError(response);
    }

    if (response.status === 204) return {} as T;
    return response.json();
  }

  private async tryRefresh(): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE}/auth/refresh`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh_token: this.refreshToken }),
      });
      if (response.ok) {
        const tokens: TokenPair = await response.json();
        this.setTokens(tokens);
        return true;
      }
      return false;
    } catch {
      return false;
    }
  }

  private async parseError(response: Response): Promise<Error> {
    try {
      const data: ApiError = await response.json();
      return new Error(data.error?.message || `HTTP ${response.status}`);
    } catch {
      return new Error(`HTTP ${response.status}`);
    }
  }

  // ── Auth endpoints ──────────────────────────────────────────────────
  async login(email: string, password: string): Promise<TokenPair> {
    const tokens = await this.request<TokenPair>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
    this.setTokens(tokens);
    return tokens;
  }

  async register(data: {
    email: string;
    full_name: string;
    password: string;
    role?: string;
    tenant_id?: string;
  }) {
    return this.request("/auth/register", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  async getProfile() {
    return this.request("/auth/me");
  }

  // ── Institution endpoints ───────────────────────────────────────────
  async listInstitutions(page = 1, pageSize = 25) {
    return this.request(
      `/institutions/?page=${page}&page_size=${pageSize}`
    );
  }

  async createInstitution(data: { name: string; slug: string; domain?: string }) {
    return this.request("/institutions/", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  async getInstitution(id: string) {
    return this.request(`/institutions/${id}`);
  }

  async listBatches(institutionId: string) {
    return this.request(`/institutions/${institutionId}/batches`);
  }

  async createBatch(
    institutionId: string,
    data: { name: string; year: number }
  ) {
    return this.request(`/institutions/${institutionId}/batches`, {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  // ── Student endpoints ───────────────────────────────────────────────
  async listStudents(params?: { batch_id?: string; page?: number; page_size?: number }) {
    const searchParams = new URLSearchParams();
    if (params?.batch_id) searchParams.set("batch_id", params.batch_id);
    if (params?.page) searchParams.set("page", String(params.page));
    if (params?.page_size) searchParams.set("page_size", String(params.page_size));
    return this.request(`/students/?${searchParams}`);
  }

  async createStudent(data: {
    email: string;
    full_name: string;
    batch_id: string;
    career_track?: string;
  }) {
    return this.request("/students/", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  async getStudent(id: string) {
    return this.request(`/students/${id}`);
  }
}

export const api = new ApiClient();
export type { TokenPair, ApiError };
