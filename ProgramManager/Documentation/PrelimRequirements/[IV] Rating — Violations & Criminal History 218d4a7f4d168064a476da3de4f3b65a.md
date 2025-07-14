# [IV] Rating — Violations & Criminal History

# Violations & Criminal History

## **1 — Violations**

Driver Points Violations determine how many risk points are added to a driver’s record based on the **severity** and **recurrence** of traffic offenses. Points are applied automatically through integration or entered manually by an agent if not returned by the system. These points are totaled to assign a factor using the **`Driver Points Table`**.

### **1.1 — Violation Intake & Deduplication Logic**

Violations can be sourced from two separate systems:

**A. Verisk Integration**

- System automatically fetches violation history using Verisk.
- Each violation includes:
    - Verisk code (e.g., `241000`)
    - Description
    - Violation date
- Returned violations are **locked and non-editable** in the UI (read-only for agents).

**B. Manual Agent Entry**

- If a customer discloses a violation not present in the Verisk return, the agent can **manually add** it.
- Agent must:
    - Choose violation from system list
    - Provide date
    - Indicate the number of occurrences (1st, 2nd, 3rd+)
- System will block manual entry of violations already returned by Verisk to avoid duplication.

### **1.2 — DCS Integration (Criminal History Mapping)**

- A second integration is run simultaneously with DCS.
- If DCS returns a **criminal offense** flagged with an **alcohol-related marker (`A`)**, it is mapped to the existing `DWI` row in the **`Driver Points Violations Table`**.
- If multiple DCS alcohol offenses are returned, each is counted as a separate occurrence and assigned points accordingly.
- DCS entries are logged in the same timeline and point total as Verisk/Manual.

### **1.3  — Driver Points Violation Assignment Rules**

Each violation maps to a point value based on how many times it has occurred for the same driver:

| **Severity Level
`(editable)`** | **First Offense
`(editable)`** | **Second Offense
`(editable)`** | **Third+ Offense
`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- | --- |
| Major (e.g., DUI, Drug Offenses) | 6 | 6 | 6 | **`Select from program term options`** | On |
| Severe (e.g., Aggravated Assault, Auto Theft) | 5 | 5 | 5 | **`Select from program term options`** | On |
| Major Moving or Licensing Violations | 3 | 5 | 5 | **`Select from program term options`** | On |
| Minor Moving or Licensing Violations | 1 | 1 | 2 | **`Select from program term options`** | On |
| Non-Ratable or Informational Only | 0 | 0 | 0 | **`Select from program term options`** | On |
| `Add/delete severity level` |  |  |  |  |  |

### **1.4 — System Behaviour**

- The system **sums all violation points** across all sources (Verisk, DCS, Manual).
- Total point value maps to a multiplier in the **Driver Points Factor Table**.

Example:

- Agent sees:
    - DWI (DCS returned) = 6 pts
    - Speeding (manual) = 1 pt
    - Total = **7 points**
- Rating engine fetches the **driver point factor for 7 points** and applies it to all coverage lines.
    - Violation type
    - Number of prior occurrences (1st, 2nd, or 3rd+)

### **1.5 — Driver Points Violations Table**

| **Mapped From

`(non-editable)`

`(Dropdown, multi-select); Options are: 
- Verisk
- Manual
- DCS`**
 | **Code

`(non-editable)

(Dropdown, multi-select) with fields based on "mapped from" field`** | **Driver Points Violations
`(editable)`** | **Severity Level
`Dropdown; chose from severity level table`** | **`System generated based on severity level`** | **`System generated based on severity level`** | **`System generated based on severity level`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  | **Description** |  | **1ST** | **2ND** | **3RD** |  |  |
| Verisk | 241000 | ACCIDENT | Severe | 5 | 5 | 5 | **`Select from program term options`** | On |
| Verisk | 242100 | ACCIDENT - AT FAULT (MA SURCHARGEABLE ACCIDENT) | … | … | … | … | **`Select from program term options`** | On |
| Verisk | 242110 | ACCIDENT - AT FAULT PERSONAL INJURY |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 242120 | ACCIDENT - AT FAULT PROPERTY DAMAGE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 242200 | ACCIDENT - NO FAULT ESTABLISHED |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 242230 | ACCIDENT - NO FAULT ESTABLISHED DEATH |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 242210 | ACCIDENT - NO FAULT ESTABLISHED PERSONAL INJURY |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 242220 | ACCIDENT - NO FAULT ESTABLISHED PROPERTY DAMAGE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | ACCIDENT AT-FAULT |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | ACCIDENT NOT AT-FAULT |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | ACCIDENT WITH PEDESTRIAN |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 570410 | ADDITIONAL LIGHTING EQUIPMENT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 580035 | ADMINISTRATIVE DENIAL |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 580010 | ADMINISTRATIVE MESSAGE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 580020 | ADMINISTRATIVE REVIEW |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 580030 | ADMINISTRATIVE SUSPENSION/REVOCATION/CANCELLATION/DISQ |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | AGGRAVATED ASSAULT WITH AN AUTO |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 311836 | AID OR ABET, RACING |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | ALL OTHER MAJOR MOVING VIOLATIONS |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | ALL OTHER MAJOR NON-MOVING VIOLATIONS |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | ALL OTHER MINOR MOVING VIOLATIONS |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | ALL OTHER MINOR NON-MOVING VIOLATIONS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111410 | ALLOW INTOXICATED PERSON TO DRIVE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | ALLOW UNLAWFUL OPERATION OF VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | ALLOWING UNLICENSED DRIVER TO DRIVE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | ALTERED OR FORGED VIN |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111820 | ASSAULT WITH MOTOR VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | ATTEMPTING TO ELUDE POLICE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111925 | ATTEMPTING TO SHOOT FROM OR AT A MOTOR VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | AUTO THEFT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 428220 | AVOID TRAFFIC CONTROL DEVICE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | AVOIDING TRAFFIC CONTROL DEVICE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 574210 | AXLE WEIGHT LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 429170 | BOTH HANDS MUST BE ON HANDLEBARS |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | CARELESS AND IMPRUDENT DRIVING |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 311230 | CARELESS DRIVING |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 428340 | CARRY UNSECURED PASSENGERS < 18 ON BACK OF TRUCK W/O ADULT PRESENT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 428335 | CARRY UNSECURED PASSENGERS IN OPEN AREA OF VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | CELL PHONE VIOLATION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 573200 | CERTAIN SAFETY DEVICE REQUIRED FOR EXPLOSIVE CARGO |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | CHANGING DRIVER IN MOVING VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | CHANGING LANES WHEN UNSAFE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | COASTING WITH GEARS DISENGAGED |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 573300 | COMPLY WITH REGULATIONS IF CARRYING HAZARDOUS MATERIAL |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | CONSUMING ALCOHOL WHILE DRIVING |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | CONVICTION OF INSURANCE FRAUD |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 584040 | CRIMINAL ACTIVITY OTHER THAN FELONY |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | CRIMINAL NEGLIGENCE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 428320 | CROSS FIRE HOSE WITHOUT CONSENT |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | CROSSING CENTER MEDIAN |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | CROSSING DIVIDED HIGHWAY |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | CROSSING YELLOW LINE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 512621 | DAMAGE AND/OR TAMPER WITH MOTOR VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 241370 | DAMAGED UNATTENDED VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 429615 | DANGEROUS OPERATION OF SNOWMOBILE/ATV/WATERCRAFT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 551100 | DEFAULT ON INSTALLMENT PAYMENT/PAY FOR DAMAGES |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 571100 | DEFECTIVE BRAKE EQUIPMENT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 571000 | DEFECTIVE BRAKES - GENERAL |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 579100 | DEFECTIVE BRAKES-MOTORCYCLE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DEFECTIVE EQUIPMENT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 576200 | DEFECTIVE EXHAUST SYSTEM, EXCESSIVE NOISE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 579010 | DEFECTIVE HEADLAMP-MOTORCYCLE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 576300 | DEFECTIVE HORN; NOT EQUIPPED WITH HORN |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 570370 | DEFECTIVE LIGHTS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 570100 | DEFECTIVE OR NO LAMPS - GENERAL |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 570435 | DEFECTIVE SCHOOL BUS EQUIPMENT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 579020 | DEFECTIVE TAIL LAMP-MOTORCYCLE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 575100 | DEFECTIVE TOWING EQUIPMENT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 570170 | DEFECTIVE TURN SIGNALS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 572210 | DEFECTIVE WIPERS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 583200 | DEPOSIT NAILS, GLASS, ON ROAD WAY, LITTERING/BURNING |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DISOBEYING OFFICIAL TRAFFIC SIGNAL/CONTROL DEVICE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DISOBEYING POLICE ORDERS |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DISPLAYING ALTERED DRIVER'S LICENSE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DISPLAYING ANOTHER PERSON'S DRIVER'S LICENSE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DISPLAYING COUNTERFEIT DRIVER'S LICENSE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 130140 | DISQUALIFICATION |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DISREGARD OF NO PASSING ZONE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DISREGARD OF SAFETY |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DISREGARDING STOP LIGHT |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DISREGARDING STOP SIGN |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111316 | DRINKING/USE OF CONTROLLED SUBSTANCES WHILE OPERATING MOTOR VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 428140 | DRIVE - MOUNTAIN ROAD TO STAY RIGHT, ETC |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421120 | DRIVE BELOW POSTED MINIMUM |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 428110 | DRIVE ON WRONG SIDE OF DIVIDED HIGHWAY |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421015 | DRIVE OVER MAXIMUM SPEED LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111130 | DRIVE TO ENDANGER |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421110 | DRIVE TOO SLOW AS TO IMPEDE TRAFFIC |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 428600 | DRIVE WHERE PROHIBITED |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 131245 | DRIVE WHILE LICENSE DENIED OR DISQUALIFIED |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 131246 | DRIVE WHILE LICENSE IS BARRED |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111105 | DRIVE WHILE LICENSE IS SUSP/REVO/DENI/DISQ/CANC RESULTING IN ACCI |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 131247 | DRIVE WHILE LICENSE IS WITHDRAWN |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 131240 | DRIVE WHILE LICENSE SUSPENDED/REVOKED/CANCELLED |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 131248 | DRIVE WHILE OUT OF SERVICE IS IN EFFECT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 428400 | DRIVE WHILE VISION/HEARING OBSTRUCTED |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111314 | DRIVE WITH BLOOD ALCOHOL CONTENT GREATER THAN 0.10 PERCENT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 531250 | DRIVE WITHOUT VALID LICENSE FOR VEHICLE OPERATION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 241210 | DRIVER IN PERSONAL INJURY/DEATH ACCIDENT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 241220 | DRIVER IN PROPERTY DAMAGE ACCIDENT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 431260 | DRIVER IN VIOLATION OF RESTRICTION OF LICENSE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 431270 | DRIVER TO CARRY LICENSE AND DISPLAY ON DEMAND |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 241230 | DRIVER TO FILE WRITTEN ACCIDENT REPORT WITHIN A GIVEN TIME PERIOD |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DRIVER'S VIEW OBSTRUCTED |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DRIVING AT NIGHT WITHOUT LIGHTS |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DRIVING ON LEFT SIDE OF ROADWAY |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DRIVING ON SHOULDER |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DRIVING ON SIDEWALK OR PARKWAY |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DRIVING ON WRONG SIDE OF ROAD |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DRIVING OVER FIRE HOSE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DRIVING SCHOOL BUS WHILE INTOXICATED |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DRIVING THE WRONG WAY |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DRIVING THROUGH SAFETY ZONE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DRIVING TOO FAST FOR CONDITIONS |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DRIVING TOO SLOW FOR CONDITIONS |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DRIVING UNDER MINIMUM SPEED LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DRIVING W/O VALID LICENSE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DRIVING WHILE UNLICENSED |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DRIVING WITH EXPIRED LICENSE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DRIVING WITH REVOKED LICENSE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DRIVING WITH SUSPENDED LICENSE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DRIVING WITHOUT A LICENSE OR PERMIT |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DRIVING WITHOUT OWNER'S CONSENT |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DRIVING WRONG WAY ON ONE-WAY |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DROVE LEFT OF CENTER |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DUI |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111312 | DUI - ALCOHOL |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111318 | DUI - ALCOHOL BY A MINOR |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111321 | DUI - ALCOHOL/DRUGS BY A MINOR |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111311 | DUI - ALCOHOL/DRUGS RESULTING IN DEATH/INJURY |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111310 | DUI - ALCOHOL/DRUGS RESULTING IN PROP DAMAGE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DUI - ALCOHOL/LIQUOR |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111320 | DUI - COMBINATION ALCOHOL/DRUGS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111315 | DUI - DEFFERRED/NON CONVICTION PROBATION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111328 | DUI - DRUGS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111319 | DUI - DRUGS BY A MINOR |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DUI - DRUGS/OPIATES |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111300 | DUI - GENERAL |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 311334 | DUI - SUBSTANCES NOT INTENDED TO INTOXICATE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DUPLICATE DRIVER'S LICENSE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | DWAI |  |  |  |  | **`Select from program term options`** | On |
| Manual/DCS | **`Logged any time "A (alcohol)" is returned as a criminal offense from DCS.`** | DWI |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | EDUCATION PROGRAM REQUIRED |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421200 | ENERGY SPEED |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | EVADING ARREST |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 429180 | EXCEDE OR VIOLATE PASSENGER OR CARGO LIMITS OF MOTORCYCLE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 590020 | EXCEEDING HOURS ON DUTY LIMITATIONS (MISCELLANEOUS DUTY FAILURE) |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421080 | EXCESSIVE ACCELERATION |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | EXCESSIVE ACCELERATION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 576220 | EXCESSIVE FUMES AND/OR SMOKE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 576210 | EXCESSIVE NOISE UNSPECIFIED CAUSE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421035 | EXCESSIVE SPEED |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | EXCESSIVE SPEEDING |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 331255 | EXPIRED OR NO DRIVER LICENSE(CDL OR PERMIT) |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 536655 | EXPIRED OR NO LICENSE PLATES OR DECAL/STICKER |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 557300 | FAIL TO APPEAR |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 423110 | FAIL TO CANCEL SIGNAL |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 576600 | FAIL TO CARRY FLARES AND/OR OTHER DEVICES |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 531580 | FAIL TO COMPLY WITH LICENSE PROVISIONS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 570340 | FAIL TO DIM HEADLIGHTS FOLLOWING VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 570330 | FAIL TO DIM HEADLIGHTS FOR APPROACHING VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 570220 | FAIL TO DISPLAY LAMPS AND/OR FLAGS ON PROJECTED LOAD |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 552100 | FAIL TO FILE FUTURE PROOF FOLLOWING CONVICTION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 552200 | FAIL TO FILE FUTURE PROOF REASON UNSPECIFIED |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 552000 | FAIL TO MAINTAIN FINANCIAL RESPONSIBILTY (REQUIRED INSURANCE, ETC.) |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 427300 | FAIL TO MAINTAIN SAFE DISTANCE FOR PASSING |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 557250 | FAIL TO MAKE REQUIRED PAYMENT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 552300 | FAIL TO MEET OTHER REQUIREMENTS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 552400 | FAIL TO MEET SECURITY FOLLOWING ACCIDENT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 241310 | FAIL TO NOTIFY FOLLOWING DISABLING ACCIDENT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 582110 | FAIL TO NOTIFY OF CHANGE IN NAME AND/OR ADDRESS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 425600 | FAIL TO OBEY POLICE OFFICER, FIREMAN AND/OR OTHER AUTHORIZED PERSON |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 425200 | FAIL TO OBEY SIGNAL AT RAILROAD CROSSING |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 425100 | FAIL TO OBEY TRAFFIC CONTROL SIGNAL, GENERAL |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 425300 | FAIL TO OBEY TRAFFIC DEVICE (SIGN,ETC) |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 427110 | FAIL TO PASS ON RIGHT/OPPOSITE DIRECTION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 557000 | FAIL TO PAY CHILD SUPPORT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 557100 | FAIL TO PAY TAXES |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 557200 | FAIL TO PAY TOLL |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 241350 | FAIL TO REPORT ACCIDENT - UNSPECIFIED |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 552500 | FAIL TO SHOW INSURANCE CERTIFICATE OR DOCUMENT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 423100 | FAIL TO SIGNAL INTENTION TO TURN, STOP OR PASS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 423200 | FAIL TO SOUND HORN, MOUNTAIN ROAD |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 241320 | FAIL TO STOP AFTER ACCIDENT - UNSPECIFIED |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 241240 | FAIL TO STOP AFTER PERSONAL INJURY/DEATH ACCIDENT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 241250 | FAIL TO STOP AFTER PROPERTY DAMAGE ACCIDENT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 241330 | FAIL TO STOP AFTER STRIKING ATTENDED VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 241340 | FAIL TO STOP AFTER STRIKING UNATTENDED VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 541360 | FAIL TO STOP AND RENDER AID |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 541260 | FAIL TO STOP AND REPORT ACCIDENT WITH ANIMAL |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 425330 | FAIL TO STOP AND YIELD RIGHT OF WAY AT STOP SIGN |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 425210 | FAIL TO STOP AT REQUIRED RAILROAD GRADE CROSSING |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 425500 | FAIL TO STOP/YIELD - ENTERING FROM PRIVATE ROAD AND/OR DRIVEWAY |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 425900 | FAIL TO STOP-UNSPECIFIED, OTHER |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 536320 | FAIL TO SURRENDER OUT-OF-STATE PERMIT/LICENSE: MORE THAN 1 LICENSE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 536330 | FAIL TO SURRENDER SUSPENDED AND/OR REVOKED LICENSE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 428330 | FAIL TO USE CHILD RESTRAINT SYSTEM |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 570230 | FAIL TO USE HEADLIGHTS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 570350 | FAIL TO USE PROPER HEADLIGHT BEAM |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 428300 | FAIL TO USE RESTRAINT SYSTEM (SEAT BELT) |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 424100 | FAIL TO YIELD - GENERAL |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 424300 | FAIL TO YIELD RIGHT OF WAY AT INTERSECTION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 424400 | FAIL TO YIELD TO EMERGENCY VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 424200 | FAIL TO YIELD TO PEDESTRIAN, GENERALLY |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 424500 | FAIL TO YIELD TO VEHICLE / PERSON IN HIGHWAY CONST. / MAINT. |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 424600 | FAIL TO YIELD WHEN OVERTAKEN |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | FAILED TO DRIVE SINGLE LANE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | FAILED TO STOP & RENDER AID |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | FAILURE OF DUTY |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | FAILURE TO CONTROL SPEED |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | FAILURE TO CONTROL VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | FAILURE TO DIM HEADLIGHTS |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | FAILURE TO DISPLAY LICENSE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | FAILURE TO EXCHANGE INFO AFTER ACCIDENT |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | FAILURE TO GIVE TURN SIGNAL |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | FAILURE TO KEEP RIGHT |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | FAILURE TO PAY TOLL |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | FAILURE TO SOUND HORN |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | FAILURE TO STOP AND GIVE INFORMATION |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | FAILURE TO STOP FOR APPROACHING TRAIN |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | FAILURE TO STOP FOR RAILROAD CROSSING |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | FAILURE TO STOP FOR RED LIGHT |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | FAILURE TO STOP FOR STOP SIGN |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | FAILURE TO STOP OR REMAIN STOPPED FOR A SCHOOL BUS |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | FAILURE TO UNDERGO TESTING UNDER IMPLIED CONSENT L |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | FAILURE TO USE IGNITION INTERLOCK DEVICE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | FAILURE TO USE TURN SIGNAL |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | FAILURE TO WEAR SEAT BELT |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | FAILURE TO YIELD (PEDESTRIAN) |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | FAILURE TO YIELD RIGHT OF WAY |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | FAILURE TO YIELD TO EMERGENCY VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 536340 | FALSE AFFIDAVIT TO MATTER REQUIRING LICENSE PROVISIONS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 553000 | FALSE CERTIFICATION |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | FALSE LICENSE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | FALSE REGISTRATION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 241213 | FATAL ACCIDENT |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | FELONY INVOLVING A MOTOR VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111810 | FLEEING AND/OR ATTEMPTING TO ELUDE POLICE OFFICER |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | FLEEING FROM POLICE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | FOLLOWING IMPROPERLY |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | FOLLOWING TOO CLOSE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 428815 | FOLLOWING TOO CLOSELY/TAILGATING |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 536350 | FRAUDULENT LICENSE EXAMINATION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111850 | FREQUENCY OF SERIOUS VIOLATIONS TO INDICATE DISREGARD |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | GIVING FALSE ACCIDENT REPORT |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | GIVING IMPROPER SIGNAL |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 574220 | GROSS WEIGHT LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111880 | HABITUAL OFFENDER |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111870 | HABITUALLY RECKLESS OR NEGLIGENT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 579210 | HANDLEBARS NO MORE THAN 15 INCHES ABOVE SEAT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 570240 | HEADLAMPS IMPROPERLY ADJUSTED-CAUSING GLARE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 570190 | HEADLAMPS REQUIRED |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 574110 | HEIGHT AND LENGTH RESTRICTIONS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111750 | HIT & RUN - FELONY ACCIDENT |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | HIT AND RUN |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111510 | HOMICIDE BY VEHICLE, NEGLIGENT HOMICIDE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | HOMICIDE WITH A MOTOR VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | HOV LANE VIOLATION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 536390 | IDENTIFICATION CARD VIOLATION |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | ILLEGAL OR IMPROPER BACKING |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | ILLEGAL OR IMPROPER TURN |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | ILLEGAL PASS ON RIGHT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111910 | ILLEGAL POSESSION OF WEAPON INCLUDING FIREARM |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111900 | ILLEGAL POSSESS/USE/TRAFFIC DRUGS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111400 | ILLEGAL POSSESSION OF ALCOHOL AND/OR DRUGS IN MOTOR VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111401 | ILLEGAL POSSESSION OF CONTROLED SUSBSTANCE IN A MOTOR VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | ILLEGAL TRANSPORTATION OF ALCOHOL |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 570360 | ILLEGAL USE OF LIGHTS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 428500 | IMPEDE STREETCAR BY DRIVING ON TRACKS |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | IMPEDING TRAFFIC MOVEMENT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 426500 | IMPROPER BACKING |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | IMPROPER BACKING |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 428210 | IMPROPER CROSSING OF DIVIDED HIGHWAY |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | IMPROPER DRIVING |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | IMPROPER ENTERING/LEAVING TURNPIKE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | IMPROPER MERGING INTO TRAFFIC |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 428310 | IMPROPER OPERATION OF EMERGENCY VEHICLE OR SCHOOL BUS BY DRIVER |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 427100 | IMPROPER PASSING |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | IMPROPER PASSING |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | IMPROPER PASSING OF A SCHOOL BUS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 423300 | IMPROPER SIGNAL GIVEN (HAND, ARM, LAMP) |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | IMPROPER START |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | IMPROPER TOWING OR PUSHING OF A VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 428700 | IMPROPER TOWING, GENERALLY |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 426100 | IMPROPER TURN |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 426110 | IMPROPER TURN AROUND (NOT U TURN) |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 576750 | IMPROPER USE OF EQUIPMENT |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | IMPROPER USE OF LANE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 428200 | IMPROPER USE OF OR ACCESS ONTO AND/OR FROM CONTROL ACCESS HIGHWAY |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 575120 | IMPROPER USE OF TOWING EQUIPMENT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 578100 | IMPROPER VEHICLE USE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 428800 | INATTENTION TO OPERATION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 428805 | INATTENTIVE DRIVING - HANDHELD DEVICE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | INCREASE SPEED WHILE BEING PASSED |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 428510 | INTERFERE WITH FUNERAL/MOVING PROCESSION/EMERGENCY VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 557400 | INVALID CHECKS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111520 | INVOLUNTARY (VEHICULAR) MANSLAUGHTER |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | INVOLUNTARY MANSLAUGHTER |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 575110 | LACK OF NECESSARY TOWING EQUIPMENT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 428100 | LANE VIOLATION |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | LEAVE VEHICLE WHILE ENGINE RUNNING |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | LEAVING THE SCENE OF AN ACCIDENT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 584130 | LEAVING VEHICLE UNATTENDED WITH ENGINE RUNNING |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 536640 | LICENSE PLATE VIOLATION - GENERAL |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | LICENSE SUSPENDED |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 536400 | LICENSE/REGISTRATION VIOLATION - GENERAL |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | LICENSED LESS THAN 2 YEARS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 536410 | LICENSEE NOT ENTITLED AND/OR GAVE WRONG INFORMATION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 536420 | LICENSEE SHALL NOT PERMIT UNLAWFUL USE OF LICENSE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 530010 | LICENSING ACTION |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | LIGHT VIOLATIONS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 574140 | LOAD EXTENDING BEYOND VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 536645 | LOAN REGISTRATION OR PLATES TO ANOTHER |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | LOANED DRIVER'S LICENSE TO ANOTHER PERSON |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 590025 | LOGBOOK VIOLATION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 571200 | MAINTENANCE ON BRAKES |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421050 | MAXIMUM LIMIT AS ALTERED LOCAL AUTHORITIES |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421020 | MAXIMUM SPEED LIMIT 30 URBAN, 55 OTHER |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 429110 | MAY NOT OPERATE MOTORCYCLE MORE THAN 2 ABREAST IN LANE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 580000 | MISCELLANEOUS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 584020 | MISCELLANEOUS-DEPARTMENT OF MOTOR VEHICLES DESIGNATION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 536650 | MISSING, DEFACED OR OBSURED LICENSE PLATES |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | MOTOR VEHICLE INSPECTION VIOLATION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 429300 | MOTORCYCLE OPERATOR TO WEAR HELMET AND/OR EYE PROTECTION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 429140 | MOTORCYCLE PROHIBITED FROM PASSING VEHICLE IN SAME LANE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 429000 | MOTORCYCLE VIOLATION - GENERAL |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 579230 | MOTORCYCLE WITH PASSENGER SHALL HAVE FOOTRESTS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 428999 | MULTIPLE VIOLATIONS |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | MURDER WITH A MOTOR VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 536430 | MUTILATED LICENSE/REGISTRATION/ID/TITLE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | NEGLIGENT COLLISION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111210 | NEGLIGENT DRIVING |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | NEGLIGENT DRIVING |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111215 | NEGLIGENT DRIVING WITH PROPERTY DAMAGE AND/OR BODILY INJURY |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | NEGLIGENT HOMICIDE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | NO CHAUFFER'S LICENSE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 131200 | NO DRIVERS LICENSE - GENERAL |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | NO EVIDENCE OF LIABILITY INSURANCE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | NO LIABILITY INSURANCE INFORCE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 582120 | NO LICENSE, REGISTRATION OR INSURANCE ID IN POSSESSION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 572000 | NO MIRRORS, DEFECTIVE MIRRORS |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | NO MOTORCYCLE QUALIFICATION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 131440 | NO OPERATION ON FOREIGN LICENSE DURING SUSPENSION AND/OR REVOCATION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 590010 | NO OR IMPROPER TRIP PERMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 573310 | NO PERSON SHALL CARRY HAZARDOUS MATERIALS W/O CERTIFICATE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 588150 | NO PERSON SHALL INTERFERE WITH TRAFFIC CONTROL DEVICE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 555110 | NO PROOF OF INSURANCE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 579030 | NO REFLECTOR-MOTORCYCLE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 570210 | NO REFLECTORS |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | NO VEHICLE INSPECTION STICKER |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 428610 | NO VEHICLE SHALL DRIVE THROUGH SAFETY ZONE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 572200 | NO WINDSHIELD WIPERS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 554000 | NON-PAYMENT OF JUDGMENT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 428620 | NOT TO ENTER INTERSECTION IF SPACE INSUFFICIENT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 428520 | OBSTRUCT TRAFFIC - GENERAL |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | OBSTRUCTING POLICE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | OBSTRUCTING TRAFFIC |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | OBTAINING LICENSE BY MISREPRESENTATION |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | OPEN CONTAINER VIOLATION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 584030 | OPENED DOOR INTO MOVING TRAFFIC |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 576500 | OPERATE VEHICLE IN UNSAFE CONDITION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111305 | OPERATING ATV/SNOWMOBILE/WATERCRAFT UNDER THE INFLUENCE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | OPERATING DURING LIFE SUSPENSION |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | OPERATING OUT OF CLASS |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | OPERATING WHERE PROHIBITED |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | OPERATING WITH DEFECTIVE EQUIPMENT |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | OPERATING WITHOUT INSURANCE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 576800 | OPERATING WITHOUT REQUIRED EQUIPMENT, OTHER |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | OTC, UM, PIP OR MED PAY CLAIM |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 576700 | OTHER DEFECTIVE/IMPROPER EQUIPMENT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 579500 | OTHER DEFECTIVE/IMPROPER EQUIPMENT-MOTORCYCLE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 579550 | OTHER MOTORCYCLE EQUIPMENT VIOLATION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 428900 | OTHER MOVING VIOLATION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 584050 | OTHER NON-MOVING VIOLATIONS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 574000 | OTHER PERMIT VIOLATIONS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 574160 | OTHER PROJECTING LOAD VIOLATION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 584060 | OTHER VIOLATION-DEPARTMENT OF MOTOR VEHICLES DESIGNATION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 480040 | OUT OF STATE VIOLATION (UNSPECIFIED) |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | OUT-OF-STATE DRIVER LICENSE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | OVERHEIGHT VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | OVERLENGTH VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 427400 | OVERTOOK STREETCAR |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 427200 | OVERTOOK VEHICLE STOPPED TO ALLOW PEDESTRIAN MOVEMENT |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | OVERWEIGHT VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | OWI |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 555100 | OWNER NOT TO PERMIT OPERATION OF UNINSURED VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 555300 | OWNER SHALL NOT PERMIT UNLAWFUL OPERATION OF VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 555200 | OWNER SHALL RETURN REGISTRATION IF INSURANCE CANCELED |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 567200 | PARKING - BRIDGE,TUNNEL,ETC |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 560100 | PARKING - GENERAL |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 568100 | PARKING AS TO IMPEDE TRAFFIC |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 567400 | PARKING BETWEEN DIVIDED HIGHWAY AND/OR ROAD |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 561500 | PARKING BETWEEN SAFETY ZONE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 568200 | PARKING DOUBLE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 566200 | PARKING IN CROSSWALK |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 562100 | PARKING IN FRONT OF PUBLIC AND/OR PRIVATE DRIVEWAY |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 561400 | PARKING IN HANDICAPPED DESIGNATED AREA |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 566100 | PARKING IN INTERSECTION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 567300 | PARKING ON ANY CONTROL ACCESS HIGHWAY |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 567100 | PARKING ON MAIN TRAVELED WAY |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | PARKING ON ROADWAY |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 565100 | PARKING ON SIDEWALK |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 563100 | PARKING TO BLOCK EMERGENCY FACILITIES, FIRE HYDRANT/STATION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 568300 | PARKING UNSAFELY (FAIL TO SET BRAKES, ETC.) |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 561100 | PARKING WHERE PROHIBITED BY TRAFFIC CONTROL DEVICE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 566300 | PARKING WITHIN 20 FEET OF CROSSWALK |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 564100 | PARKING WITHIN 50 FEET OF RAILROAD CROSSING |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 583300 | PARTS OF PASSENGER PROJECTED FROM VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 427600 | PASSED STOPPED SCHOOL BUS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 571300 | PERFORMANCE OF BRAKES |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 574120 | PERMIT REQUIRED FOR EXCESSIVE SIZE AND WEIGHT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 531450 | PERMIT UNAUTHORIZED MINOR TO DRIVE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 531460 | PERMIT UNAUTHORIZED PERSON TO DRIVE - GENERAL |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 531470 | PERMIT UNLICENSED DRIVER TO DRIVE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 429160 | PERSON ON MOTORCYCLE MAY NOT ATTACH TO ANOTHER VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 556100 | PERSON SHALL NOT DRIVE UNINSURED VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 556200 | PERSON SHALL NOT GIVE FALSE INFORMATION IN REQUESTED REPORT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 531510 | PERSONS UNDER 18 NOT TO DRIVE FOR HIRE/PUBLIC PASSENGER |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 426400 | POSITION AND METHOD OF TURN - GENERAL |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111395 | POSSESSION |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | POSSESSION OF CONTROLLED SUBSTANCE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | POSSESSION OF DECEPTIVE DRIVER LICENSE/ID |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | POSSESSION OF MORE THAN ONE DRIVERS LICENSE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111405 | POSSESSION OF OPEN ALCOHOL CONTAINER |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 580050 | PRAYER FOR JUDGEMENT (NC) |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111835 | PREARRANGED RACING |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | PROHIBITED U-TURN |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | PROTECTIVE HEADGEAR VIOLATION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 530150 | PROVISIONAL SUSPENSION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 583400 | PUSHED VEHICLE IN DANGEROUS MANNER |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111830 | RACING |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | RACING |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 512630 | RECEIVE STOLEN VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | RECKLESS DRIVING |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111110 | RECKLESS DRIVING, WILLFUL AND WANTON DISREGARD |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 241500 | REFUSAL TO REVEAL ID - AFTER ACCIDENT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 241505 | REFUSAL TO REVEAL ID - FATAL ACCIDENT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 241515 | REFUSAL TO REVEAL ID - PROPERTY ACCIDENT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111335 | REFUSAL TO SUBMIT TO CHEMICAL TEST |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111340 | REFUSAL TO SUBMIT TO CHEMICAL TEST PERSON UNDER 21 |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 574240 | REFUSAL TO SUBMIT TO WEIGHING |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | REFUSE BREATH TEST |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 581200 | REGISTRATION/TITLE VIOLATION - GENERAL |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 330130 | REINSTATEMENT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 512622 | REMOVE AND/OR FALSIFY VEHICLE AND/OR ENGINE IDENTIFICATION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 570420 | RESTRICTION ON LAMPS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 130120 | REVOCATION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 429200 | RIDERS ON MOTORCYCLE - GENERAL |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 579600 | RV/SNOWMOBILE EQUIPMENT VIOLATION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 572300 | SAFETY GLAZING REQUIRED |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111840 | SCHOOL BUS VIOLATION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111920 | SHOOTING FROM OR AT A MOTOR VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421140 | SPECIAL SPEED LIMITATIONS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421010 | SPEED - GENERAL |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421410 | SPEED 10-14 OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421420 | SPEED 10-19 OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421490 | SPEED 11 PLUS OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421320 | SPEED 1-10  OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421445 | SPEED 11-14 OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421450 | SPEED 11-15 OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421470 | SPEED 11-19 OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421480 | SPEED 11-20 OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421327 | SPEED 1-14  OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421330 | SPEED 1-15  OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421340 | SPEED 1-19  OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421350 | SPEED 1-25  OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421300 | SPEED 1-5   OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421520 | SPEED 15 PLUS OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421530 | SPEED 15 TO 29 OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421510 | SPEED 15-20 OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421560 | SPEED 16 PLUS OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421540 | SPEED 16-20 OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421550 | SPEED 16-25 OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421305 | SPEED 1-9   OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421611 | SPEED 20 PLUS OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421624 | SPEED 21 PLUS OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421615 | SPEED 21-25 OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421620 | SPEED 21-30 OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421653 | SPEED 25 PLUS OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421634 | SPEED 25-34 OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421635 | SPEED 26 PLUS OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421625 | SPEED 26-30 OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421630 | SPEED 26-35 OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421752 | SPEED 31 PLUS OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421751 | SPEED 31-35 OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421770 | SPEED 35 PLUS OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421762 | SPEED 36 PLUS OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421760 | SPEED 36-40 OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421763 | SPEED 40 PLUS OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421775 | SPEED 41-45 OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421880 | SPEED 46 PLUS OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421370 | SPEED 6-10  OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421380 | SPEED 6-20  OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421360 | SPEED 6-9   OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421390 | SPEED 9-15  OVER LIMIT |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | SPEED CONTEST |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421030 | SPEED GREATER THAN REASONABLE OR PRUDENT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421070 | SPEED IN SCHOOL ZONE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421075 | SPEED IN WORK ZONE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421060 | SPEED LIMIT FOR TRUCKS AND BUSES |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421640 | SPEED OVER 29 MPH IN EXCESS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421150 | SPEED WHILE TOWING |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | SPEEDING |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | SPEEDING IN A CONSTRUCTION ZONE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | SPEEDING IN A SCHOOL ZONE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 428810 | SPINNING WHEELS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 570510 | SPOT, FOG, AUXILIARY LAMP VIOLATION |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | SQUEALING OR SCREECHING TIRES |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 259999 | SR-22 FILING |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 421040 | STATE SPEED ZONES AS NOTED BY SIGNS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 241270 | STRIKE A LEGALLY STOPPED CAR |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 130110 | SUSPENSION |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | SUSPENSION (CHARGEABLE) |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 512610 | THEFT OF MOTOR VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111930 | THROW HARMFUL OBJECTS ON THE HIGHWAY & ROADWAYS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111420 | TRANSPORT LIQUOR/ALCOHOL ILLEGALLY |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111421 | TRANSPORT LIQUOR/ALCOHOL TO A MINOR |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | TRANSPORTATION OF HAZARDOUS MATERIALS |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 570180 | TURN SIGNALS LAMPS REQUIRED |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | TURNED ACROSS DIVIDED SECTION |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | TURNED WHEN UNSAFE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111710 | UNAUTHORIZED USE OF MOTOR VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 429620 | UNLAWFUL GOLF CART OPERATION ON HIGHWAY |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 583100 | UNLAWFUL NOISE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 576100 | UNLAWFUL POSSESSION OF VEHICLE EQUIPMENT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 429600 | UNLAWFUL RV/SNOWMOBILE/MOTORCYCLE OPERATION ON CONTROLLED HIGHWAY |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 429610 | UNLAWFUL RV/SNOWMOBILE/TRACTOR OPERATION ON HIGHWAY |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 531530 | UNLAWFUL TO DISPLAY ALTERED, CANCELED/SUSPENDED/REVOKED LICENSE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 531540 | UNLAWFUL TO DISPLAY ANOTHER PERSONS LICENSE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 536550 | UNLAWFUL TO LEND LICENSE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 574230 | UNLAWFUL TO OPERATE IN EXCESS OF REGULATED LOAD |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | UNLAWFUL USE OF DRIVER'S LICENSE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | UNRESTRAINED CHILD |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 426200 | UNSAFE LANE CHANGE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | UNSAFE LANE CHANGE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 428750 | UNSAFE OPERATION/ DRIVING |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | UNSAFE OPERATOR |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | UNSAFE PARK |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | UNSAFE SPEED |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | UNSAFE STANDING |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | UNSAFE START |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 428830 | UNSAFE START FROM PARKED POSITION |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | UNSAFE STOP |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 576400 | UNSAFE TIRES |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 426300 | UNSAFE U-TURN |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 574150 | UNSECURED AND/OR UNCOVERED LOAD, LEAKING LOAD |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 531555 | UNSPECIFIED LIC PLATE/PERMIT MISREP,UNLAWFUL USE LIC PLATE/PERMIT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 531560 | UNSPECIFIED LICENSE MISREPRESENTATION, UNLAWFUL USE OF LICENSE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | UNVERIFIABLE MVR |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 536570 | USE OF FALSE NAME AND/OR OTHER STATEMENT TO OBTAIN LICENSE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | USE OF ILLEGAL DRIVER LICENSE/ID |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111600 | USE OF MOTOR VEHICLE IN COMMISSION OF FELONY |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 576900 | USE OF RADAR DETECTOR (CT, DC, VA, NY) |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | USE OF WIRELESS DEVICE FOR TEXT-BASED COMM |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | USE OF WIRELESS DEVICE WITHOUT HANDSFREE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 573100 | VEHICLE CARRYING HAZARDOUS MATERIALS TO DISPLAY PLACARD |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | VEHICLE EMISSIONS SUSPENSION |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 574100 | VEHICLE EXCEEDS SIZE AND/OR WEIGHT, GENERALLY |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 581100 | VEHICLE INSPECTION VIOLATION |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | VEHICULAR INJURY |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | VEHICULAR MANSLAUGHTER |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 572100 | VIEW THROUGH WINDSHIELD OBSTRUCTED |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | VIOLATING SAFETY ZONE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 585200 | VIOLATION BY PEDESTRIAN |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 584100 | VIOLATION OF CONDITIONS OF PROBATION |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | VIOLATION OF DRIVER'S LICENSE RESTRICTION |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | VIOLATION OF INSTRUCTION PERMIT |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | VIOLATION OF LIQUOR LAW |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 584110 | VIOLATION OF PROMISE TO APPEAR |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | VIOLATION OF PROMISE TO APPEAR |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111317 | VIOLATION OF SPECIAL ALCOHOL PROVISION BY MINOR |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 573000 | VIOLATION OF TRANSFER OF HAZARDOUS MATERIAL, GENERALLY |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 111530 | VIOLATION OF VEHICLE LAW RESULTING IN DEATH, MANSLAUGHTER |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 241400 | VIOLATION RESULTING IN ACCIDENT |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 585100 | VIOLATION WITH NON-MOTOR VEHICLE |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 570250 | WARNING LIGHTS TO BE DISPLAYED WHEN TRUCK STOPPED |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 570260 | WARNING LIGHTS TO BE DISPLAYED WHEN VEHICLE DISABLED |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 574130 | WIDTH NOT TO EXCEED CERTAIN LENGTH |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 530160 | WITHDRAWAL |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 536630 | WITHDRAWAL OF CONSENT FOR MINORS LICENSE |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | WRONG DIRECTION AROUND TRAFFIC ISLAND |  |  |  |  | **`Select from program term options`** | On |
| Manual |  | WRONG DIRECTION DIVIDED STREET |  |  |  |  | **`Select from program term options`** | On |
| Verisk | 428130 | WRONG WAY - GENERAL |  |  |  |  | **`Select from program term options`** | On |
|  | `Add/delete MANUAL row only`

`Code-related rows are fetched from Verisk/DCS integration` |  |  |  |  |  |  |  |

### **1.6 — Driver Points**

Driver points represent the **cumulative risk level** associated with a driver's history of violations and infractions. This factor increases proportionally with the number of points on record, and impacts rating across all major coverage lines.

- **Driver Points**: Integer values ranging from 0 to 50+
- The **cumulative risk level** is determined by aggregating the violations from the “Driver Points” section

| **Points
`(editable)`** | **Round Factor By
`(editable)`** | **BI
`(editable)`** | **PD
`(editable)`** | **UMBI
`(editable)`** | **UMPD
`(editable)`** | **MED
`(editable)`** | **PIP
`(editable)`** | **COMP
`(editable)`** | **COLL
`(editable)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 1 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 2 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| 3 | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| ... |  | ... | ... | ... | ... | ... | ... | ... | ... |  |  |
| 50+ | 2 | #.## | #.## | #.## | #.## | #.## | #.## | #.## | #.## | **`Select from program term options`** | On |
| `Add/delete driver points option` |  |  |  |  |  |  |  |  |  |  |  |

## **2 — Criminal History**

The Criminal History integration fetches offense records from DCS. The system evaluates these records against configurable driver and policy eligibility rules. Only **alcohol-related offenses (Category A)** are mapped to the rating engine via the **Driver Violations Table** (specifically to `DWI`). All others are for **eligibility checks only**.

### **2.1 — Offense Ingestion and Categorization**

| **Field
`(non-editable)`** | **Source
`(non-editable)`** | **Notes
`(non-editable)`** |
| --- | --- | --- |
| `Offense Code` | DCS return | Unique identifier |
| `Offense Code Description` | DCS return | Textual description |
| `Offense Code Level` | DCS return | Code (e.g. `F1`, `MB`, `BLANK`) |
| `Offense Code Level Description`
 | DCS return | Plaintext (e.g., “MISDEMEANOR - CLASS B”) |
| **Criminal Offense Category** | **MGA configured** | Required. Select one: `A` (Alcohol), `M` (Misdemeanor), `F` (Felony) |

### **2.2 — Offense Category Definitions Table**

| **Category
`(editable)`** | **Label
`(editable)`** | **Description
`(editable)`** |
| --- | --- | --- |
| A | Alcohol | Indicates alcohol-related offenses. Used for rating (mapped to DWI). |
| M | Misdemeanor | Minor criminal offense, used for eligibility. |
| F | Felony | Major criminal offense, used for eligibility. |
| `Add/edit/remove category` |  |  |

### **2.3 — Alcohol Category Mapping (Rating Rule)**

- If a returned offense is tagged with **A (Alcohol)**:
    - It is **mapped directly to the DWI row** in the **Driver Violations Table**.
    - If multiple A-tagged offenses are returned, each is treated as a separate occurrence.
    - Points are assigned using existing DWI point structure based on occurrence count.

### **2.4 — Criminal History Table**

| **Mapped From

`(non-editable)`

`(Dropdown, multi-select); Options are: 
- DCS`**
 | **Code

`(non-editable) 

(Dropdown, multi-select) with fields based on "mapped from" field`** | **Offense Code Description

`Fetched from DCS integation`** | **Offense Code Level**

**`Fetched from DCS integation`** | **Offense Code Level Description

`Fetched from DCS integation`** | **Criminal Offense Category

`(editable) — Options are from "Category Definitions Table"`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DCS | 00020000 | ARREST DATA NOT CLEAR | BLANK | UNKNOWN | M | **`Select from program term options`** | On |
| DCS | 00020000 | TEST | BLANK | UNKNOWN | M | **`Select from program term options`** | On |
| DCS | 00020000 | ARREST DATA NOT RECEIVED | BLANK | UNKNOWN | M | **`Select from program term options`** | On |
| DCS | 00029999 | FINGERPRINT SUPPORTED DISPOSITION | BLANK | UNKNOWN | M | **`Select from program term options`** | On |
| DCS | 00030000 | DECEASED | BLANK | UNKNOWN | M | **`Select from program term options`** | On |
| DCS | 00040000 | OUT OF STATE PROBATION TRANSFER | BLANK | UNKNOWN | M | **`Select from program term options`** | On |
| DCS | 00050000 | OUT OF STATE PAROLE TRANSFER | BLANK | UNKNOWN | M | **`Select from program term options`** | On |
| DCS | 00060000 | SEX OFFENDER REGISTRATION | BLANK | UNKNOWN | M | **`Select from program term options`** | On |
| DCS | 01010000 | TREASON | BLANK | UNKNOWN | M | **`Select from program term options`** | On |
| DCS | 01020000 | TREASON MISPRISON | BLANK | UNKNOWN | M | **`Select from program term options`** | On |
| DCS | 01030000 | ESPIONAGE | BLANK | UNKNOWN | M | **`Select from program term options`** | On |
| DCS | 01040000 | SABOTAGE | BLANK | UNKNOWN | M | **`Select from program term options`** | On |
| DCS | 01050000 | SEDITION | BLANK | UNKNOWN | M | **`Select from program term options`** | On |
| DCS | 01060000 | SELECTIVE SERVICE | BLANK | UNKNOWN | M | **`Select from program term options`** | On |
| DCS | 01990000 | SOVEREIGNTY -FREE TEXT | BLANK | UNKNOWN | M | **`Select from program term options`** | On |
| DCS | 02010000 | DESERTION | BLANK | UNKNOWN | M | **`Select from program term options`** | On |
| DCS | 02990000 | MILITARY-FREE TEXT | BLANK | UNKNOWN | M | **`Select from program term options`** | On |
| DCS | 03010000 | ILLEGAL ENTRY | BLANK | UNKNOWN | M | **`Select from program term options`** | On |
| DCS | 03020000 | FALSE CITIZENSHIP | BLANK | UNKNOWN | M | **`Select from program term options`** | On |
| DCS | 03030000 | SMUGGLING ALIENS | BLANK | UNKNOWN | M | **`Select from program term options`** | On |
| DCS | 03990000 | IMMIGRATION-FREE TEXT | BLANK | UNKNOWN | M | **`Select from program term options`** | On |
| DCS | 03990001 | MISREPRESENT CHILD AS FAMILY MEMBER ENTRY PORT | MB | MISDEMEANOR - CLASS B | M | **`Select from program term options`** | On |
| DCS | 09000000 | HOMICIDE-FREE TEXT | BLANK | UNKNOWN | M | **`Select from program term options`** | On |
| DCS | 09000001 | MURDER INTENTIONALLY CAUSES DEATH | F1 | FELONY - 1ST DEGREE | F | **`Select from program term options`** | On |
| DCS | 09000002 | MURDER INTENDS SBI CAUSING DEATH | F1 | FELONY - 1ST DEGREE | F | **`Select from program term options`** | On |
| DCS | 09000003 | MURDER WHILE COMMITTING FELONY | F1 | FELONY - 1ST DEGREE | F | **`Select from program term options`** | On |
| DCS | 09000004 | CAPITAL MURDER POLICE OFFICER OR FIREMAN | FX | FELONY - CAPITAL FELONY | F | **`Select from program term options`** | On |
| DCS | 09000005 | CAPITAL MURDER WHILE COMMITTING CITED OFFENSES | FX | FELONY - CAPITAL FELONY | F | **`Select from program term options`** | On |
| DCS | 09000006 | CAPITAL MURDER REMUNERATION | FX | FELONY - CAPITAL FELONY | F | **`Select from program term options`** | On |
| DCS | 09000007 | CAPITAL MURDER ESCAPING PENAL INSTITUTION | FX | FELONY - CAPITAL FELONY | F | **`Select from program term options`** | On |
| DCS | 09000008 | CAPITAL MURDER IN PENAL INSTITUTION | FX | FELONY - CAPITAL FELONY | F | **`Select from program term options`** | On |
| DCS | 09000009 | CAPITAL MURDER MULTIPLE | FX | FELONY - CAPITAL FELONY | F | **`Select from program term options`** | On |
| DCS | 09000010 | VOLUNTARY MANSLAUGHTER | F2 | FELONY - 2ND DEGREE | F | **`Select from program term options`** | On |
| DCS | 09000011 | INVOLUNTARY MANSLAUGHTER | F3 | FELONY - 3RD DEGREE | F | **`Select from program term options`** | On |
|  | … | … | … | … | … | … |  |
|  | `Cannot manually add/delete rows. Codes are fetched from DCS integration` |  |  |  |  |  |  |

### **2.5 — Driver Eligibility Rules**

1. **Time Frame Options**:
    - **`3_years`**: Offenses within last 3 years
    - **`5_years`**: Offenses within last 5 years
    - **`10_years`**: Offenses within last 10 years
    - **`historical`**: All offenses regardless of age
2. **Threshold Logic**:
    - **`max_allowed`**: Maximum permitted offenses before triggering unacceptability
    - System evaluates as: **`(actual_count > max_allowed) → unacceptable`**
3. **Category Handling**:
    - **`M`**: Misdemeanor offenses only
    - **`F`**: Felony offenses only
    - **`M&F`**: Combined count of Misdemeanors and Felonies

### **2.6 — Driver Eligibility Rules Table**

This governs individual driver eligibility based on **criminal history**.

| **Category
`(editable; dropdown)`** | **Time Frame
`(editable; dropdown)`** | **Max Allowed Offenses
`(editable; number)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- |
| M | 3 years | 0 | **`Select from program term options`** | On |
| M | 10 years | 1 | **`Select from program term options`** | On |
| M | Historical | 2 | **`Select from program term options`** | On |
| F | 5 years | 0 | **`Select from program term options`** | On |
| F | Historical | 1 | **`Select from program term options`** | On |
| M & F | Historical | 1 | **`Select from program term options`** | On |
| `Add/delete driver eligibility rule` |  |  |  |  |

### **2.7 — Policy Eligibility Rules Table**

This evaluates **aggregate driver history** on a policy to determine if the **entire policy is ineligible**.

| **Category
`(editable; dropdown)`** | **Time Frame
`(editable; dropdown)`** | **Max Allowed Offenses
`(editable; number)`** | **Applied for the Following Terms
`Multi-select`** | **Supported (On/Off)
`(editable)`** |
| --- | --- | --- | --- | --- |
| M | 3 years | 1 | **`Select from program term options`** | On |
| M | 10 years | 2 | **`Select from program term options`** | On |
| M | Historical | 3 | **`Select from program term options`** | On |
| F | 5 years | 1 | **`Select from program term options`** | On |
| F | Historical | 2 | **`Select from program term options`** | On |
| M & F | Historical | 2 | **`Select from program term options`** | On |
| `Add/delete driver eligibility rule` |  |  |  |  |

### **2.8 — System Behavior and UI Handling**

**Agent-Facing Alerts**

- **Driver-Level Alert**
    - Message:
        
        > "This driver is flagged as ineligible due to prior history. Unable to proceed."
        > 
    - Displayed when a driver's criminal history violates configured limits.
    - Does not surface specific charges.
- **Policy-Level Alert (Quote Summary or Bind Attempt)**
    - Message:
        
        > "Policy flagged due to ineligible driver history. Unable to proceed."
        > 
    - Prevents bind if configured to enforce hard stop.

**Privacy and Disclosure Notes**

- No criminal charge descriptions are shown to agents in alerts.