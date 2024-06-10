import {HttpClient} from '@angular/common/http';
import {Component, OnInit} from '@angular/core';

@Component({
    selector: 'app-predict',
    templateUrl: './predict.component.html',
    styleUrls: ['./predict.component.sass']
})
export class PredictComponent implements OnInit {

    DiseaseSymptoms = []

    SelectedSymptoms!: string[];
    symptom: string = ''

    predictedData: {
        predicted_disease: string,
        dis_des: string,
        my_precautions: string[],
        medications: [],
        my_diet: [],
        workout: []
    } | null = null
    predicting: boolean = false
    errorMsg: string = '';

    constructor(private http: HttpClient) {
    }

    ngOnInit(): void {
        this.SelectedSymptoms = new Array<string>()
        this.getSymptoms()
    }

    addSymptom() {
        this.errorMsg = ''
        this.predictedData = null
        if (!this.SelectedSymptoms.includes(this.symptom) && this.SelectedSymptoms.length <= 17)
            this.SelectedSymptoms.push(this.symptom)
        this.symptom = ''
    }

    removeSymptom(i: number) {
        console.log(this.SelectedSymptoms[i]);
        this.SelectedSymptoms = this.SelectedSymptoms.filter(symptom => {
            return this.SelectedSymptoms[i] !== symptom
        })
    }

    predict() {
        this.errorMsg = ''
        this.predicting = true
        if (this.SelectedSymptoms.length >= 1) {
            this.predictDisease(this.SelectedSymptoms).subscribe((r: any) => {
                this.predictedData = r.msg
                this.predicting = false
            }, (err: any) => {
                this.predicting = false
                this.errorMsg = 'Error occurred while predicting check Server terminal for more info' +
                    'Error: ' + err.error.meesage + ''
            })
        } else {
            this.predicting = false
            this.errorMsg = 'Select at-least one symptom'
        }

    }

    getSymptoms() {
        this.http.get("http://localhost:8000/api/symptoms/").subscribe({
            next: (r: any) => {
                this.DiseaseSymptoms = r.symptoms
            }
        })
    }

    predictDisease(symptoms: string[]) {
        let data = symptoms.join(",")
        return this.http.post("http://localhost:8000/api/predict_disease/", {symptoms: data})
    }
}
