import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';  // Injection de HttpClient
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'  // Cette ligne est optionnelle si tu utilises un service autonome
})
export class SearchService {

  private apiUrl = 'https://api.example.com/search';

  constructor(private http: HttpClient) {}  // Injection de HttpClient

  search(query: string): Observable<any> {
    return this.http.get(`${this.apiUrl}?q=${query}`);
  }
} 