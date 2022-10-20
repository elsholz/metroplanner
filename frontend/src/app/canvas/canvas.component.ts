import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-canvas',
  templateUrl: './canvas.component.html',
  styleUrls: ['./canvas.component.scss']
})
export class CanvasComponent implements OnInit {
  @Input()
  public scrollable: boolean = true;

  constructor() { }

  ngOnInit(): void {
    console.log("Am I scrollable?", this.scrollable)
  }

}
