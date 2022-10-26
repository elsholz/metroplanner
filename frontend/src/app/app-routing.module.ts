import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EditorComponent } from './editor/editor.component';
import { ExploreComponent } from './explore/explore.component';
import { ImpressumComponent } from './impressum/impressum.component';
import { IndexComponent } from './index/index.component';
import { PricingComponent } from './pricing/pricing.component';
import { ProfileComponent } from './profile/profile.component';
import { RoadmapComponent } from './roadmap/roadmap.component';
import { SupportComponent } from './support/support.component';
import { ViewerComponent } from './viewer/viewer.component';

const routes: Routes = [
  { path: '', component: IndexComponent },
  { path: 'support', component: SupportComponent },
  { path: 'impressum', component: ImpressumComponent },
  { path: 'roadmap', component: RoadmapComponent },
  // { path: 'pricing', component: PricingComponent },
  { path: 'explore', component: ExploreComponent },
  { path: 'profile', component: ProfileComponent },
  { path: 'edit/:planid', component: EditorComponent },
  { path: 'p/:shortlink', component: ViewerComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
