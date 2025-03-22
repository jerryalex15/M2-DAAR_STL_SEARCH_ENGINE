import { ChangeDetectorRef, Component, HostListener } from '@angular/core';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { SearchService } from '../services/search.service';
import { NgIf, CommonModule } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatInputModule } from '@angular/material/input';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatIconModule } from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';

@Component({
  selector: 'app-search',
  standalone: true,
  templateUrl: './search.component.html',
  styleUrl:'./search.component.scss',
  imports: [
    CommonModule,
    NgIf,
    MatFormFieldModule,
    ReactiveFormsModule,
    MatSelectModule,
    MatInputModule,
    MatToolbarModule,
    MatIconModule,
    MatButtonModule,
    MatCardModule,
    MatGridListModule,
    MatSlideToggleModule,
    FormsModule,
  ]
})
export class SearchComponent {
  searchForm: FormGroup;
  result: any[] = [];
  suggestions: any[] = [];

  isKeywordSearch: boolean = true;
  isRegexSearch: boolean = false;
  isAdvancedKeywordSearch: boolean = false;
  isAdvancedRegexSearch: boolean = false;

  gridCols = 3;  // Valeur par défaut pour grands écrans

  constructor(private fb: FormBuilder, private searchService: SearchService, private cdr: ChangeDetectorRef) {
    this.searchForm = this.fb.group({
      searchType: ['keyword'],
      keyword: [''],
      pattern: [''],
      centrality_type: ['pagerank'],
      max_suggestions: [10]
    });

    this.updateGridCols(); // Appel initial
  }


  @HostListener('window:resize', ['$event'])
  onResize() {
    this.updateGridCols();
  }

  ngAfterViewInit() {
    this.updateGridCols(); // Assurer que le DOM est chargé
  }

  updateGridCols() {
    if (typeof window !== 'undefined') {
      const width = window.innerWidth;
      this.gridCols = width < 800 ? 1 : width < 1200 ? 2 : 3;
    }
  }
  setSearchType(type: string): void {
    // Réinitialiser tous les états à false avant de définir celui sélectionné
    this.isKeywordSearch = false;
    this.isRegexSearch = false;
    this.isAdvancedKeywordSearch = false;
    this.isAdvancedRegexSearch = false;

    const searchFormControls = this.searchForm.controls;

    if (type === 'keyword') {
      this.isKeywordSearch = true;
      this.isRegexSearch = false;
      this.isAdvancedKeywordSearch = false;
      this.isAdvancedRegexSearch = false;
      searchFormControls['pattern'].setValue(null);
    } else if (type === 'regex') {
      this.isRegexSearch = true;
      this.isKeywordSearch = false;
      this.isAdvancedKeywordSearch = false;
      this.isAdvancedRegexSearch = false;
      searchFormControls['keyword'].setValue(null);
    } else if (type === 'advancedKeyword') {
      this.isAdvancedKeywordSearch = true;
      this.isKeywordSearch = false;
      this.isRegexSearch = false;
      this.isAdvancedRegexSearch = false;
      searchFormControls['pattern'].setValue(null);
    } else if (type === 'advancedRegex') {
      this.isAdvancedRegexSearch = true;
      this.isKeywordSearch = false;
      this.isRegexSearch = false;
      this.isAdvancedKeywordSearch = false;
      searchFormControls['keyword'].setValue(null);
    }

    // Déclencher la détection des changements pour forcer l'actualisation du DOM
    this.cdr.detectChanges();
  }

  onSearch() {
    const formData = this.searchForm.value;
  
    if (this.isKeywordSearch && formData.keyword.trim()) {
      this.searchService.searchByKeyword(formData.keyword).subscribe({
        next: response => (this.result = response),
        error: error => console.error('Erreur de recherche par mot-clé:', error)
      });
    } else if (this.isRegexSearch && formData.pattern.trim()) {
      this.searchService.searchByRegex(formData.pattern).subscribe({
        next: response => (this.result = response),
        error: error => console.error('Erreur de recherche par regex:', error)
      });
    } else {
      console.warn('Veuillez entrer un mot-clé ou une expression régulière.');
    }
  }

  onAdvancedSearch() {
    const formData = this.searchForm.value;

    this.searchService.rankAndSuggest(formData).subscribe({
      next: response => {
        this.result = response.ranked_results;
        this.suggestions = response.top_suggestions;
      },
      error: error => console.error('Erreur lors de la recherche avancée:', error)
    });
  }
}