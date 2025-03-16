import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { SearchService } from '../services/search.service';
import { NgIf, JsonPipe, CommonModule } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select'; 
import { MatInputModule } from '@angular/material/input';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatIconModule } from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';

@Component({
  selector: 'app-search',
  standalone: true,
  templateUrl: './search.component.html',
  styleUrl:'./search.component.scss',
  imports: [
    CommonModule,
    JsonPipe,
    NgIf,
    MatFormFieldModule,
    ReactiveFormsModule,
    MatSelectModule,
    MatInputModule,
    MatToolbarModule,
    MatIconModule,
    MatButtonModule
  ]
})
export class SearchComponent {
  searchForm: FormGroup;
  result: any = null;

  constructor(private fb: FormBuilder, private searchService: SearchService) {
    this.searchForm = this.fb.group({
      keyword: [''],
      pattern: [''],
      centrality_type: ['closeness'],
      max_suggestions: [10]
    });
  }

  onSubmit() {
    const formData = this.searchForm.value;
    this.searchService.search(formData).subscribe(response => {
      this.result = response;
    }, error => {
      console.error('Erreur lors de la requête :', error);
    });
  }
}