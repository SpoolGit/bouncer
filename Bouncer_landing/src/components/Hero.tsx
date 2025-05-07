
import { Button } from "@/components/ui/button";
import { ChartPie, Shield, Database } from "lucide-react";

const Hero = () => {
  return (
    <section className="pt-24 pb-16 md:pt-32 md:pb-24 bg-finance-gray">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
          <div className="animate-fade-in">
            <h1 className="text-4xl md:text-5xl font-bold text-finance-navy mb-4">
              AI-Powered<br />
              <span className="text-finance-teal">Financial Audit</span> Solutions
            </h1>
            <p className="text-xl text-gray-600 mb-8 leading-relaxed">
              Transform your financial auditing process with our advanced AI technology. 
              Reduce errors, save time, and gain deeper insights into your financial data.
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <Button className="btn-primary">Request Demo</Button>
              <Button className="btn-secondary" onClick={() => window.open('https://bouncer.streamlit.app/', '_blank')}>
				Try It Now!
			  </Button>
            </div>
          </div>
          
          <div className="relative animate-fade-in">
            <div className="bg-white p-8 rounded-lg shadow-xl relative z-10">
              <div className="absolute -top-12 -right-12 w-24 h-24 bg-finance-teal opacity-50 rounded-full filter blur-xl"></div>
              <div className="absolute -bottom-8 -left-8 w-16 h-16 bg-finance-navy opacity-20 rounded-full filter blur-lg"></div>
              
              <div className="relative z-20">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                  <div className="flex flex-col items-center p-4 border border-gray-200 rounded-lg bg-white">
                    <ChartPie className="w-10 h-10 text-finance-teal mb-2" />
                    <p className="text-center text-sm font-medium">Anomaly Detection</p>
                  </div>
                  <div className="flex flex-col items-center p-4 border border-gray-200 rounded-lg bg-white">
                    <Shield className="w-10 h-10 text-finance-teal mb-2" />
                    <p className="text-center text-sm font-medium">Fraud Prevention</p>
                  </div>
                  <div className="flex flex-col items-center p-4 border border-gray-200 rounded-lg bg-white">
                    <Database className="w-10 h-10 text-finance-teal mb-2" />
                    <p className="text-center text-sm font-medium">Data Analysis</p>
                  </div>
                  <div className="flex flex-col items-center p-4 border border-gray-200 rounded-lg bg-white">
                    <svg className="w-10 h-10 text-finance-teal mb-2" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M3 9H7L12 4L17 9H21M3 15H7L12 20L17 15H21" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                    <p className="text-center text-sm font-medium">Pattern Recognition</p>
                  </div>
                </div>
                <div className="mt-6 w-full h-10 bg-gray-100 rounded-md overflow-hidden">
                  <div className="w-3/4 h-full bg-gradient-to-r from-finance-navy to-finance-teal rounded-md"></div>
                </div>
                <p className="mt-2 text-xs text-gray-500">AI-Powered Analysis: 75% More Efficient</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
