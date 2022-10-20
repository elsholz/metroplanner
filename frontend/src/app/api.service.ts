import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

const config = {
  "domain": "dev-twa5tnu1.eu.auth0.com",
  "clientId": "8mxekg7iDQSgxabarihl5KfynOjirudy",
  "audience": "https://ich-hab-plan.de/api/",
  "apiUri": "http://localhost:4200",
  "appUri": "http://localhost:4200",
  "errorPath": "/error"
}



@Injectable({
  providedIn: 'root',
})
export class ApiService {
  constructor(private http: HttpClient) { }

//  ping$(): Observable<any> {
//    console.log(config.apiUri);
//    let res = this.http.get(`${config.apiUri}/api/_user`);
//    console.log("This is the API Resukt:", res)
//
//    return res
//  }

  getCurrentUserProfile$(includePlanData: boolean, includeColorThemeData: boolean): Observable<any> {
    console.log(config.apiUri);
    let res = this.http.get(
      `${config.apiUri}/api/_user${includeColorThemeData || includePlanData ? '?' : ''}`+
      `${includePlanData ? 'includePlanData' : ''}${includePlanData&&includeColorThemeData ? '&' : ''}${includeColorThemeData ? 'includeColorThemeData' : ''}`
      );
    console.log("This is the API Resukt:", res)

    return res
  }
}
