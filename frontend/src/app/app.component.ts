import { Component } from '@angular/core';
import { AuthService, User } from '@auth0/auth0-angular';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  public profile?: User | null = null
  public loggedIn?: boolean = false
  public darkMode: boolean = false

  title = 'Ich-hab-Plan.de'
  constructor(
    public auth: AuthService
  ) {

  }

  ngOnInit(): void {
    this.auth.user$.subscribe(
      (user: any) => {
        if (user) {
          this.profile = user
          this.loggedIn = true
          console.log("hello, World!", user)
        } else {
          this.profile = null
          this.loggedIn = false
        }
      },
    );
  }
  logout() {
    console.log("Logout button pressed")
    this.auth.logout()
    this.loggedIn = false
  }

  toggleDarkMode() {
    console.log("Dar mode toggled")
    this.darkMode != this.darkMode
  }
}