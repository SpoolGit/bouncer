
const HowItWorks = () => {
  const steps = [
    {
      number: "01",
      title: "Data Integration",
      description: "Connect your financial systems and data sources to our secure platform with just a few clicks."
    },
    {
      number: "02",
      title: "AI Analysis",
      description: "Our powerful AI algorithms analyze your financial data, identifying patterns, anomalies, and potential issues."
    },
    {
      number: "03",
      title: "Risk Assessment",
      description: "Receive a comprehensive risk assessment with prioritized findings and recommendations."
    },
    {
      number: "04",
      title: "Actionable Insights",
      description: "Get clear, actionable insights and recommendations to improve your financial processes and compliance."
    }
  ];

  return (
    <section id="how-it-works" className="py-16 md:py-24 bg-finance-navy text-white">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto text-center mb-12 md:mb-20">
          <span className="bg-finance-teal/20 text-finance-teal font-medium px-4 py-2 rounded-full text-sm mb-4 inline-block">Process</span>
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            How <span className="text-finance-teal">AuditAI</span> Works
          </h2>
          <p className="text-xl text-gray-300">
            Our streamlined process harnesses the power of artificial intelligence to transform your financial auditing.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {steps.map((step, index) => (
            <div 
              key={index} 
              className="relative"
            >
              <div className="bg-finance-teal/10 border border-finance-teal/20 p-8 rounded-xl h-full">
                <div className="text-5xl font-bold text-finance-teal/30 mb-4">
                  {step.number}
                </div>
                <h3 className="text-xl font-semibold mb-4 text-finance-teal">
                  {step.title}
                </h3>
                <p className="text-gray-300">
                  {step.description}
                </p>
              </div>
              {index < steps.length - 1 && (
                <div className="hidden md:block absolute top-1/2 -right-4 transform -translate-y-1/2 z-10">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="#0EA5E9" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="mt-16 md:mt-24 max-w-3xl mx-auto text-center">
          <p className="text-xl text-gray-300 mb-8">
            Ready to transform your financial auditing process?
          </p>
          <a 
            href="#" 
            className="btn-primary inline-block"
          >
            Schedule a Demo
          </a>
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;
