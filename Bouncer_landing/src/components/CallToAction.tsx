
import { Button } from "@/components/ui/button";

const CallToAction = () => {
  return (
    <section className="py-16 md:py-24 bg-finance-navy">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-finance-gradient rounded-xl overflow-hidden">
          <div className="p-8 md:p-12 relative">
            <div className="absolute top-0 right-0 w-1/3 h-full opacity-10">
              <svg width="100%" height="100%" viewBox="0 0 400 400" fill="none" xmlns="http://www.w3.org/2000/svg">
                <g opacity="0.2">
                  <circle cx="200" cy="200" r="150" stroke="white" strokeWidth="30"/>
                  <path d="M200 50V350" stroke="white" strokeWidth="15"/>
                  <path d="M350 200H50" stroke="white" strokeWidth="15"/>
                </g>
              </svg>
            </div>
            
            <div className="max-w-3xl mx-auto text-center relative z-10">
              <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
                Ready to Transform Your Financial Audit Process?
              </h2>
              <p className="text-xl text-gray-300 mb-8">
                Join the hundreds of companies that have revolutionized their financial auditing with our AI-powered solution.
              </p>
              <div className="flex flex-col sm:flex-row justify-center gap-4">
                <Button className="bg-white hover:bg-gray-100 text-finance-navy font-semibold py-3 px-6 rounded-md transition-colors duration-200">
                  Request Demo
                </Button>
                <Button variant="outline" className="text-white border-white hover:bg-white/10 transition-colors duration-200">
                  Contact Sales
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default CallToAction;
