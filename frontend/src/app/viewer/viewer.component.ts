import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from "@angular/router";
import { ApiService } from '../api.service';

@Component({
  selector: 'app-viewer',
  templateUrl: './viewer.component.html',
  styleUrls: ['./viewer.component.scss']
})
export class ViewerComponent implements OnInit {

  //public shortlink: String | undefined;
  public planData: any | undefined
  public shortlink: string | undefined
  public coordinateScalar: Number = 20

  json: any = JSON

  constructor(
    private route: ActivatedRoute,
    private api: ApiService,
  ) {
    this.route.params.subscribe(params => {
      console.log(params)
      this.shortlink = params["shortlink"]
      console.log("This the shortlink::", this.shortlink)


      this.api.getPlanData$(this.shortlink).subscribe({
        next: async (res) => {
          console.log("Data from the API::")
          console.log(res)
          this.planData = res
        }
      })
    });
  }

  ngOnInit(): void {

  }


}
