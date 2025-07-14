# [I] Program Definitions

# Program Definitions

### Variable

Variables are the **raw data points** gathered during the quote or application process.

Example: 

- `Driver Age = 18`
- `Driver Age = 24`
- `Driver Age = 56`

### **Attribute**

An **attribute is a group of variables** can influence rating, eligibility, or underwriting logic. Attributes are often based on driver, vehicle, or policy characteristics.

Example:

- `Driver Age`
- `Vehicle Usage Type`
- `Prior Coverage Duration`

### **Attribute Group**

A **collection of related attributes** organized by a common theme, data source, or entity type (e.g., vehicle, driver, policy). Attribute groups help streamline logic and UI layout.

Example Groups:

- **Driver Attributes:** Age, License Type, Points
- **Vehicle Attributes:** VIN Symbol, Mileage, Ownership Length
- **Policy Attributes:** Term, Payment Plan, Distribution Channel

Attribute groups are used to **logically organize** how attributes are applied and managed in the system.

### **Rating Factor**

A **numerical multiplier** applied to a base rate based on a specific value or range of an attribute. Rating factors adjust premiums up or down based on risk.

Example:

- If `Vehicle Usage = Commute > 5 mi`, apply **factor = 1.15**
- If `Driver Age = 25`, apply **factor = 1.05**

Rating factors are defined per attribute **and often vary by line of coverage.**

### **Factor Grouping**

A **composite logic structure** that applies a single rating factor based on a **combination of two or more attributes**. Factor groupings enable more nuanced risk segmentation.

Example:

- If `Vehicle Usage = Commute > 5 mi` **AND** `Vehicle Age = 2 years`, apply **factor = 1.20**
- If `Driver Age = 18` **AND** `Prior Coverage < 6 months`, apply **factor = 1.50**

Factor groupings support advanced modeling where **individual attributes alone are not sufficient** to capture the desired risk logic.