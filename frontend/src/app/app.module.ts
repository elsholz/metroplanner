import { NgModule } from '@angular/core';
import { bootstrapApplication, BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { IndexComponent } from './index/index.component';
import { ViewerComponent } from './viewer/viewer.component';
import { EditorComponent } from './editor/editor.component';
import { HeaderComponent } from './header/header.component';
import { PricingComponent } from './pricing/pricing.component';
import { ExploreComponent } from './explore/explore.component';
import { SupportComponent } from './support/support.component';
import { AuthModule } from '@auth0/auth0-angular';
import { CanvasComponent } from './canvas/canvas.component';
import { ProfileComponent } from './profile/profile.component';
import { FooterComponent } from './footer/footer.component';
import { HttpClientModule } from '@angular/common/http';

import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { AuthHttpInterceptor } from '@auth0/auth0-angular';


@NgModule({
  declarations: [
    AppComponent,
    IndexComponent,
    ViewerComponent,
    EditorComponent,
    HeaderComponent,
    PricingComponent,
    ExploreComponent,
    SupportComponent,
    CanvasComponent,
    ProfileComponent,
    FooterComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    AuthModule.forRoot({
      domain: 'dev-twa5tnu1.eu.auth0.com',
      clientId: '8mxekg7iDQSgxabarihl5KfynOjirudy',
      audience: "https://ich-hab-plan.de/api/",
      httpInterceptor: {
        allowedList: [
          `http://localhost:4200/api/_user`,
        ],
      }
    }),
    HttpClientModule
  ],
  providers: [
    BrowserModule,
    HttpClientModule,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthHttpInterceptor,
      multi: true,
    },
  ],
  bootstrap: [AppComponent],
})
export class AppModule { }
