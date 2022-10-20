import { Component, OnInit } from '@angular/core';
import { User } from '@auth0/auth0-angular';
import { AppComponent } from '../app.component';

import { HttpClient } from '@angular/common/http';
import { ApiService } from '../api.service';
import { Observable } from 'rxjs';


@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})

export class ProfileComponent implements OnInit {
  public profileData: any = null
  public JSON
  public picture: any

  constructor(
    public app: AppComponent,
    private api: ApiService,
  ) {
    this.app = app
    this.JSON = JSON
  }


  ngOnInit(): void {
    this.api.getCurrentUserProfile$(true, true).subscribe({
      next: async (res) => {
        this.profileData = res 
        this.app.auth.getUser().subscribe(
          (user) => {
            this.picture = user?.picture
          }
        )
      }
    })



    // this.app.auth.getUser().subscribe(
    //   (user: any) => {
    //     console.log("Here we go:", user)
    //     if (user) {
    //       console.log(`Calling API for user ${user.email}`)

    //       this.http
    //         .get(`http://localhost:4200/api/_user`)
    //         .subscribe((result: any) => {
    //           console.log("API-Result:", result)
    //           this.profileData = JSON.stringify( result, null, 4)
    //         });
    //     }
    //   }
    // )
  }
}
