
import { ChartBar, Shield, Database, Scale, FileText, BarChart } from "lucide-react";

const Features = () => {
  const featuresList = [
    {
      icon: <ChartBar className="h-10 w-10 text-finance-teal" />,
      title: "Automated Analysis",
      description: "AI algorithms automatically analyze and flag potential issues in financial statements and transactions."
    },
    {
      icon: <Shield className="h-10 w-10 text-finance-teal" />,
      title: "Fraud Detection",
      description: "Advanced pattern recognition identifies suspicious activities and potential fraud indicators."
    },
    {
      icon: <Database className="h-10 w-10 text-finance-teal" />,
      title: "Data Integration",
      description: "Seamlessly connect with your existing financial systems and data sources through secure APIs."
    },
    {
      icon: <Scale className="h-10 w-10 text-finance-teal" />,
      title: "Regulatory Compliance",
      description: "Stay compliant with the latest financial regulations with automated checks and validations."
    },
    {
      icon: <FileText className="h-10 w-10 text-finance-teal" />,
      title: "Audit Reports",
      description: "Generate comprehensive audit reports with actionable insights and recommendations."
    },
    {
      icon: <BarChart className="h-10 w-10 text-finance-teal" />,
      title: "Risk Assessment",
      description: "Quantify financial risks and receive predictive analytics to make informed decisions."
    }
  ];

  return (
    <section id="features" className="py-16 md:py-24 bg-white">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto text-center mb-12 md:mb-20">
          <span className="bg-finance-teal/10 text-finance-teal font-medium px-4 py-2 rounded-full text-sm mb-4 inline-block">Features</span>
          <h2 className="text-3xl md:text-4xl font-bold text-finance-navy mb-6">
            Revolutionize Financial Auditing with AI
          </h2>
          <p className="text-xl text-gray-600">
            Our cutting-edge technology streamlines the audit process,
            reducing errors and increasing efficiency.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          {featuresList.map((feature, index) => (
            <div 
              key={index} 
              className="bg-white border border-gray-100 p-8 rounded-xl shadow-sm hover:shadow-md transition-shadow duration-300"
            >
              <div className="bg-finance-teal/10 p-3 rounded-lg inline-block mb-6">
                {feature.icon}
              </div>
              <h3 className="text-xl font-semibold text-finance-navy mb-3">
                {feature.title}
              </h3>
              <p className="text-gray-600">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;
