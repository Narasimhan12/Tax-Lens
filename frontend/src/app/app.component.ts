import { Component } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { TaxWidgetComponent } from './components/tax-widget/tax-widget.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [HttpClientModule, TaxWidgetComponent],
  template: '<app-tax-widget />'
})
export class AppComponent {}
