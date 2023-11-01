class CoverageComputer:
    def __init__(self, measures_data):
        self.measures_data = measures_data

    def call(self):
        risks = self.__risks()
        risk_coverage = list(
            map(
                lambda risk: self.__risk_coverage(risk, self.measures_data),
                risks
              )
        )

        return dict(zip(risks, risk_coverage))
    
    def __risks(self):
        return list(map(
            lambda risk: risk["risk"],
            self.measures_data[0]["riskCoverage"]
        ))
    
    def __risk_coverage(self, risk, measures_data):
        measure_coverage_per_risk = list(map(
            lambda measure: self.__measure_coverage_per_risk(measure),
            measures_data
        ))

        sum_coverage = sum(map(
            lambda measure_coverage: measure_coverage[risk],
            measure_coverage_per_risk
        ))

        if sum_coverage > 100:
            return 100
        
        return sum_coverage
    
    def __measure_coverage_per_risk(self, measure):
        coverage_identifier_association =  list(map(
            lambda risk: (risk["risk"], risk["coverage"]),
            measure["riskCoverage"]
        ))

        return dict(coverage_identifier_association)
