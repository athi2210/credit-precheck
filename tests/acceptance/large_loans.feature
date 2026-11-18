Feature: Large loans need human review

  Scenario: Loan just above the limit
    Given an applicant aged 40 with good credit
    When a loan of 50,000.01 EUR is requested
    Then the request goes to a loan officer
    And no automatic approval is given
