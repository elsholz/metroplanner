import { Component, OnInit } from '@angular/core';
import { AuthService, User } from '@auth0/auth0-angular';
import { AppComponent } from '../app.component';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
})
export class HeaderComponent implements OnInit {

  constructor(
    //public app: AppComponent

    public auth: AuthService
  ) { }//this.app = app}

  ngOnInit(): void {
    // this.app.auth.user$.subscribe(
    //   (user : any) => {
    //     console.log("Header has to say:", user)
    //   }
    // )
    // this.auth.user$.subscribe(
    //   (user: any) => (this.profile = user, this.loggedIn = true, console.log(user)),
    // );
  }

  loginWithRedirect() {
    this.auth.loginWithRedirect();
  }

}
