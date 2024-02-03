#include <AFMotor.h>

char cmd[5];
int arnum = 0;
const char* cmdList[5] = { "STOP", "FRWD", "BKWD", "LEFT", "RIHT" };
enum commandEnum {
  STOP,
  FRWD,
  BKWD,
  LEFT,
  RIHT
} command;

enum motorEnum {
  A,
  B,
  C,
  D
} motor;

bool forward = false, left = false;
int action = 0;

const int irA = 19, irB = 18, irC = 21, irD = 20;
volatile int irASum, irBSum, irCSum, irDSum;
float rps[4];
float speed[4] = { 88.64, 103.41, 146.13, 125.68 };
int discHoleCount = 22;

float wheelRadius = 66.4;
int mileage;
bool turning = false;

unsigned long speedMillis, speedPreviousMillis;
int speedInterval = 100;

AF_DCMotor motorA(1);
AF_DCMotor motorB(2);
AF_DCMotor motorC(3);
AF_DCMotor motorD(4);

void ISR_sumA() {
  irASum++;
}
void ISR_sumB() {
  irBSum++;
}
void ISR_sumC() {
  irCSum++;
}
void ISR_sumD() {
  irDSum++;
}

void setup() {
  Serial.begin(115200);

  pinMode(irA, INPUT);
  pinMode(irB, INPUT);
  pinMode(irC, INPUT);
  pinMode(irD, INPUT);

  attachInterrupt(digitalPinToInterrupt(irA), ISR_sumA, RISING);
  attachInterrupt(digitalPinToInterrupt(irB), ISR_sumB, RISING);
  attachInterrupt(digitalPinToInterrupt(irC), ISR_sumC, RISING);
  attachInterrupt(digitalPinToInterrupt(irD), ISR_sumD, RISING);

  motorA.run(RELEASE);
  motorB.run(RELEASE);
  motorC.run(RELEASE);
  motorD.run(RELEASE);
}

void loop() {
  action = getSerial();
  switch (action) {
    case STOP:
      stop();
      break;
    case FRWD:
      forward = true;
      straight();
      break;
    case BKWD:
      forward = false;
      straight();
      break;
    case LEFT:
      left = true;
      turn();
      break;
    case RIHT:
      left = false;
      turn();
      break;
  }
}

float speedOutput(float speed, float rps) {
  float targetRPS = 0.5;
  float Kp = 4;

  float error = targetRPS - rps;
  speed = speed + Kp * error;
  speed = constrain(speed, 0, 255);
  return speed;
}

void setSpeeds() {
  speedMillis = millis();
  if (speedMillis - speedPreviousMillis >= speedInterval) {
    rpsUpdate();
    speed[A] = speedOutput(speed[A], rps[A]);
    speed[B] = speedOutput(speed[B], rps[B]);
    speed[C] = speedOutput(speed[C], rps[C]);
    speed[D] = speedOutput(speed[D], rps[D]);
    motorA.setSpeed(speed[A]);
    motorB.setSpeed(speed[B]);
    motorC.setSpeed(speed[C]);
    motorD.setSpeed(speed[D]);

    /*Serial.print(String(speed[A]));
    Serial.print("," + String(speed[B]));
    Serial.print("," + String(speed[C]));
    Serial.println("," + String(speed[D]));*/

    speedPreviousMillis = speedMillis;
  }
}

void stop() {
  motorA.run(RELEASE);
  motorB.run(RELEASE);
  motorC.run(RELEASE);
  motorD.run(RELEASE);
}

void straight() {
  turning = false;
  if (forward) {
    motorA.run(FORWARD);
    motorB.run(FORWARD);
    motorC.run(FORWARD);
    motorD.run(FORWARD);
  } else {
    motorA.run(BACKWARD);
    motorB.run(BACKWARD);
    motorC.run(BACKWARD);
    motorD.run(BACKWARD);
  }
  setSpeeds();
}

void turn() {
  turning = true;
  if (left) {
    motorA.run(BACKWARD);
    motorB.run(FORWARD);
    motorC.run(FORWARD);
    motorD.run(BACKWARD);
  } else {
    motorA.run(FORWARD);
    motorB.run(BACKWARD);
    motorD.run(FORWARD);
  }
  setSpeeds();
}

int getSerial() {
  if (Serial.available() == 0) return;
  if (Serial.readBytesUntil('\n', cmd, 4) >= 4) {
    while (strcmp(cmdList[arnum], cmd) != 0) {
      arnum++;
    }
    command = int(arnum);
    arnum = 0;
    cmd[5] = 0;
  }
  return command;
}

void rpsUpdate() {
  rps[A] = static_cast<float>(irASum) / discHoleCount;
  rps[B] = static_cast<float>(irBSum) / discHoleCount;
  rps[C] = static_cast<float>(irCSum) / discHoleCount;
  rps[D] = static_cast<float>(irDSum) / discHoleCount;

  if (!turning) mileage += (((rps[A] + rps[B] + rps[C] + rps[D]) / 4) * 2 * PI * wheelRadius / 2) / 10;
  Serial.println(mileage);

  irASum = irBSum = irCSum = irDSum = 0;
  /*Serial.print(String(rps[A]));
  Serial.print("," + String(rps[B]));
  Serial.print("," + String(rps[C]));
  Serial.println("," + String(rps[D]));*/
}