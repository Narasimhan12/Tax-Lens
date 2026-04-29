import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface ChatPayload {
  session_id: string;
  question: string;
  company_name?: string;
  compare_state_code?: string;
}

@Injectable({ providedIn: 'root' })
export class TaxApiService {
  private readonly baseUrl = environment.apiBaseUrl;

  constructor(private http: HttpClient) {}

  getCompanies(): Observable<{ companies: string[] }> {
    return this.http.get<{ companies: string[] }>(`${this.baseUrl}/companies`);
  }

  askChat(payload: ChatPayload): Observable<any> {
    return this.http.post(`${this.baseUrl}/chat`, payload);
  }

  getTax(companyName: string): Observable<any> {
    return this.http.get(`${this.baseUrl}/tax/${encodeURIComponent(companyName)}`);
  }
}
