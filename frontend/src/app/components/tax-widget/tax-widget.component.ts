import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TaxApiService } from '../../services/tax-api.service';

@Component({
  selector: 'app-tax-widget',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './tax-widget.component.html',
  styleUrl: './tax-widget.component.css'
})
export class TaxWidgetComponent implements OnInit {
  companies: string[] = [];
  selectedCompany = '';
  compareState = '';
  question = '';
  loading = false;
  sessionId = crypto.randomUUID();
  messages: { role: 'user' | 'assistant'; content: string }[] = [];
  latestComputation: any;

  constructor(private api: TaxApiService) {}

  ngOnInit(): void {
    this.api.getCompanies().subscribe((response) => {
      this.companies = response.companies;
      this.selectedCompany = this.companies[0] ?? '';
    });
  }

  send(): void {
    if (!this.question.trim()) {
      return;
    }
    const userText = this.question.trim();
    this.messages.push({ role: 'user', content: userText });
    this.loading = true;

    this.api
      .askChat({
        session_id: this.sessionId,
        question: userText,
        company_name: this.selectedCompany || undefined,
        compare_state_code: this.compareState || undefined
      })
      .subscribe({
        next: (response) => {
          this.messages.push({ role: 'assistant', content: response.answer });
          this.latestComputation = response.computation;
          this.loading = false;
        },
        error: (err) => {
          this.messages.push({ role: 'assistant', content: `Error: ${err.message}` });
          this.loading = false;
        }
      });

    this.question = '';
  }
}
