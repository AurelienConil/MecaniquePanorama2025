/*
    Simulation de mécanique Panorama
    Grace à une carte arduino nue, branchée en USB
    Created by Le Chat
*/

// Paramètres de simulation
unsigned long lastTime = 0;
int speed = 0;
bool rotationDirection = true; // true pour sens horaire, false pour sens anti-horaire
int acceleration = 1; // Valeur d'accélération
int maxSpeed = 9; // Vitesse maximale
int minSpeed = 0; // Vitesse minimale
int changeDirectionProbability = 5; // Probabilité de changer de direction (1/changeDirectionProbability)
int pauseProbability = 20; // Probabilité de faire une pause (1/pauseProbability)

void setup() {
  Serial.begin(115200);
  randomSeed(analogRead(0)); // Initialiser le générateur de nombres aléatoires
}

void loop() {
  unsigned long currentTime = millis();

  // Générer un nouvel état toutes les 500 ms
  if (currentTime - lastTime >= 50) {
    lastTime = currentTime;

    // Changer de direction aléatoirement
    if (random(changeDirectionProbability) == 0) {
      rotationDirection = !rotationDirection;
    }

    // Faire une pause aléatoirement
    if (random(pauseProbability) == 0) {
      speed = 0;
    } else {
      // Accélérer ou décélérer
      speed += acceleration;
      if (speed > maxSpeed) {
        speed = maxSpeed;
        acceleration = -1; // Commencer à décélérer
      } else if (speed < minSpeed) {
        speed = minSpeed;
        acceleration = 1; // Commencer à accélérer
      }
    }

    // Envoyer les données
    if (rotationDirection) {
      Serial.print("+");
    } else {
      Serial.print("-");
    }
    Serial.println(speed);
  }
}
