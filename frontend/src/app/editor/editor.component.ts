import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from "@angular/router";

@Component({
  selector: 'app-editor',
  templateUrl: './editor.component.html',
  styleUrls: ['./editor.component.scss']
})
export class EditorComponent implements OnInit {
  constructor(private route: ActivatedRoute) {
    this.route.params.subscribe(params => {
      console.log(params)
    });
  }

  ngOnInit(): void {
  }

}
