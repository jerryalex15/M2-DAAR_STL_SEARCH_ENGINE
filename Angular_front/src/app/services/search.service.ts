import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SearchService {
  private apiUrl = 'http://localhost:5001';

  constructor(private http: HttpClient) {}

  searchByKeyword(keyword: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/search_by_keyword`, { keyword });
  }

  searchByRegex(pattern: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/search_by_regex`, { pattern });
  }

  // rankAndSuggest(data: { keyword?: string; pattern?: string; centrality_type: string; max_suggestions: number }): Observable<any> {
  //   return this.http.post(`${this.apiUrl}/rank_and_suggest`, data);
  // }

  rankAndSuggest(formData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/rank_and_suggest`, formData);
  }
}
