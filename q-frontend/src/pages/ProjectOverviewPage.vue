<template>
  <q-page
    padding
    style="background-color: #001"
    dark
    class="justify-center flex row items-center"
  >
    <div class="column col col-lg-6 col-md-8 col-sm-12 text-body1 text-center">
      <div class="row q-pt-md text-white text-center">
        <div class="col-12">
          <h3>Projektvorstellung</h3>
        </div>
      </div>
      <div class="row q-pt-md text-white text-center">
        <div class="col-12">
          <q-avatar square size="150px" class="q-ma-sm">
            <img src="/icons/mpl_logo.svg" />
          </q-avatar>
        </div>
      </div>
      <div class="row text-white text-center q-pb-md">
        <div class="col-12 text-h5">METROPLANNER</div>
      </div>
      <div class="row text-white text-center q-pb-xl">
        <div class="col-12 text-italic">
          Hier findet ihr uns auch:<br />
          <q-btn
            round
            flat
            padding="sm"
            size="xl"
            icon="fa-brands fa-github"
            href="https://github.com/elsholz/metroplanner/"
          ></q-btn>
          <q-btn
            round
            flat
            padding="sm"
            size="xl"
            icon="fa-brands fa-instagram"
            href="https://instagram.com/metroplanner"
          ></q-btn>
        </div>
      </div>

      <div class="row text-white text-center">
        <div class="col-12 text-h6">Problemstellung</div>
        <hr style="background-color: white; width: 300px" />
      </div>
      <div class="row text-white text-justify q-pb-lg">
        <div class="col-12">
          <p>
            Wer in kleineren Städten und Gemeinden den ÖPNV verwenden möchte
            sieht sich häufig mit unübersichtlichen Busfahrplänen konfrontiert.
            Bei den Fahrplänen fehlt meist eine Übersicht, welche Route die
            Linie abfährt und welche Umsteige-Optionen es gibt.
          </p>
        </div>
      </div>

      <div class="row text-white text-center">
        <div class="col-12 text-h6">Zielsetzung</div>
        <hr style="background-color: white; width: 300px" />
      </div>
      <div class="row text-white text-justify q-pb-lg">
        <div class="col-12">
          <p>
            Ziel des Metroplanners ist es, die Nutzung des ÖPNVs für Jedermann
            zugänglich zu machen. Dazu müssen folgende Anforderungen erfüllt
            werden:
          </p>
          <ol>
            <li>
              Pläne müssen in kürzester Zeit auch mit schlechten
              Mobilfunk-Verbindungen abrufbar sein
            </li>
            <li>Das Design muss einheitlich und simpel sein, wie ein Diagramm</li>
            <li>
              Die Pläne müssen beliebig skalierbar sein, egal auf welchem Medium
            </li>
            <li>Gleichzeitig muss Erstellung von Plänen muss intuitiv und leichtgängig sein</li>
          </ol>
        </div>
      </div>

      <div class="row text-white">
        <div class="col-12 text-h6">Technische Hintergründe</div>
        <hr style="background-color: white; width: 300px" />
      </div>
      <div class="row text-white text-justify q-pb-lg">
        <div class="col-12">
          <p>
            Damit die Netzpläne für möglichst viele Menschen nutzbar sind und um
            eine hohe Flexibilität zu gewährleisten, ist ein entsprechendes
            technisches Konzept unabdingbar. Die Lösung muss skalierbar und
            schnell sein, Pläne müssen sowohl vom heimischen PC als auch von
            allen Mobilgeräten mit langsamen Verbindungen abrufbar sein. Auch an
            Haltestellen müssen die Netzpläne ausgehangen werden können, damit
            auch Nutzer ohne Mobilgerät die Vorteile eines Netzplans nutzen
            können.
          </p>
          <p>
            Zur Erfüllung dieser Anforderungen werden folgende Technologien
            verwendet:
          </p>
          <ul>
            <li>
              Frontend:
              <ul>
                <li>
                  Map Editor und sontige Seiten: Vue & Quasar für ein
                  ansprechendes Design und zur Erstellung eines interaktiven
                  Karten-Editors.
                </li>
                <li>
                  Kartenansicht: Reines HTML und CSS, um Ladezeiten kurz zu
                  halten, während die Pläne flexibel gestaltbar und gleichzeitig
                  beliebig skaliert werden können. Dies erlaubt auch den Export
                  der Karten in druckbare Bildformate in beliebiger Größe ohne
                  Qualitätsverlust.
                </li>
              </ul>
            </li>
            <li>
              Backend:
              <ul>
                <li>Datenbank: MongoDB</li>
                <li>API: AWS Lambda</li>
                <li>CDN: AWS CloudFront</li>
              </ul>
            </li>
            <li>
              Build Tools:
              <ul>
                <li>VCS: GitHub</li>
                <li>Deployment Pipeline: GitHub Actions</li>
                <li>
                  Infrastructure as Code: AWS CloudFormation & AWS Serverless
                  Application Model
                </li>
              </ul>
            </li>
            <li>
              Sonstiges:
              <ul>
                <li>User Management: Auth0</li>
              </ul>
            </li>
          </ul>
        </div>
      </div>

      <div class="row text-white text-center">
        <div class="col-12 text-h6">Roadmap</div>
        <hr style="background-color: white; width: 300px" />
      </div>
      <div class="row text-white text-justify q-pb-lg">
        <div class="col-12">
          Die Roadmap für das Projekt sieht folgende Milestones vor:
          <ul>
            <li>Fertigstellung der Basics: Plan Editor und Plan Viewer</li>
            <li>Optimierung des Plan Viewers um Ladezeiten zu minimieren</li>
            <li>Seite für Nutzerprofile erstellen</li>
            <li>Nutzerkonzept um Gruppen erweitern</li>
            <li>Suchfunktion Ranking nach Beliebtheit implementieren</li>
            <li>Bereitstellung eines Services zum Konvertieren der Karten in Rastergrafiken (PNG & JPG) in beliebiger Auflösung</li>
            <li>Konvertierung des Frontends in eine Progressive Web App (PWA) um Offlinenutzung zu ermöglichen</li>
          </ul>
        </div>
      </div>

      <div class="row text-white text-center">
        <div class="col-12 text-h6">Über den Ersteller</div>
        <hr style="background-color: white; width: 300px" />
      </div>
      <div class="row text-white text-center">
        <div class="col-12">Das bin ich, Hendrik:</div>
      </div>
      <div class="row text-white">
        <div class="col-12">
          <q-avatar square size="384px" class="q-ma-sm">
            <img src="/images/profile_image.jpg" />
          </q-avatar>
        </div>
      </div>
      <div class="row text-white text-center q-mb-xl">
        <div class="col-12">
          <p>
            Ich habe im Jahr 2021 mein Informatik-Studium in Mannheim
            abgeschlossen und arbeite seitdem in der Software-Entwicklung und
            Administration. Während und vor allem nach meinem Studium habe ich
            es sehr zu schätzen gelernt, durch die Liniennetzpläne in den Bussen
            und Straßenbahnen stets einen guten Überblick über die Routen und
            Umsteigepunkte zu haben.
          </p>
          <p>
            Nachdem ich wieder in meine Heimatstadt Wesel gezogen bin, fiel mir
            sofort auf, dass unserem ÖPNV-Netz ein übersichtlicher grafischer
            Plan fehlt. Da mir die Weiterentwicklung des ÖPNV sehr am Herzen
            liegt, habe ich mich dazu entschieden einen Liniennetzplan auch für
            das Stadtgebiet zu erstellen.
          </p>
          <p>
            Schnell wurde bei der Ausarbeitung des Netzplans jedoch klar, dass
            die Komplexität des Netzes sehr schnell wächst, je mehr Linien darin
            berücksichtigt werden. Selbst kleine Anpassungen des Plans waren mit
            hohem Aufwand verbunden. Nach der Erkenntnis, dass es auch an
            geeigneten Werkzeugen für die Erstellung von Netzplänen fehlt, habe
            ich mich dazu entschieden eine Webbasierte Lösung zu schaffen, um
            diesen Prozess zu vereinfachen und gleichzeitig den Zugang zu
            ÖPNV-Plänen zu vereinfachen.
          </p>
          <p>Dieses Werkeug heißt nun Metroplanner.</p>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
export default {
  setup () {
    return {}
  }
}
</script>
