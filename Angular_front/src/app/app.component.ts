import { Component } from '@angular/core';
import { SearchComponent } from './search/search.component'; 

@Component({
  selector: 'app-root',
  imports: [SearchComponent],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'Search Engine';
}
