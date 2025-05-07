
import { Facebook, Twitter, Linkedin, Instagram } from "lucide-react";

const Footer = () => {
  return (
    <footer className="bg-white py-12 md:py-16">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">
          <div>
            <a href="#" className="flex items-center mb-6">
              <span className="text-xl font-bold text-finance-navy">Audit<span className="text-finance-teal">AI</span></span>
            </a>
            <p className="text-gray-600 mb-6">
              Transforming financial auditing with powerful AI technology that reduces errors and increases efficiency.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-400 hover:text-finance-teal transition-colors duration-200">
                <Twitter size={20} />
              </a>
              <a href="#" className="text-gray-400 hover:text-finance-teal transition-colors duration-200">
                <Facebook size={20} />
              </a>
              <a href="#" className="text-gray-400 hover:text-finance-teal transition-colors duration-200">
                <Linkedin size={20} />
              </a>
              <a href="#" className="text-gray-400 hover:text-finance-teal transition-colors duration-200">
                <Instagram size={20} />
              </a>
            </div>
          </div>
          
          <div>
            <h3 className="font-semibold text-finance-navy mb-6">Product</h3>
            <ul className="space-y-4">
              <li><a href="#features" className="text-gray-600 hover:text-finance-teal transition-colors duration-200">Features</a></li>
              <li><a href="#" className="text-gray-600 hover:text-finance-teal transition-colors duration-200">Pricing</a></li>
              <li><a href="#" className="text-gray-600 hover:text-finance-teal transition-colors duration-200">Case Studies</a></li>
              <li><a href="#testimonials" className="text-gray-600 hover:text-finance-teal transition-colors duration-200">Testimonials</a></li>
            </ul>
          </div>
          
          <div>
            <h3 className="font-semibold text-finance-navy mb-6">Resources</h3>
            <ul className="space-y-4">
              <li><a href="#" className="text-gray-600 hover:text-finance-teal transition-colors duration-200">Blog</a></li>
              <li><a href="#" className="text-gray-600 hover:text-finance-teal transition-colors duration-200">Documentation</a></li>
              <li><a href="#" className="text-gray-600 hover:text-finance-teal transition-colors duration-200">Support</a></li>
              <li><a href="#" className="text-gray-600 hover:text-finance-teal transition-colors duration-200">API</a></li>
            </ul>
          </div>
          
          <div>
            <h3 className="font-semibold text-finance-navy mb-6">Company</h3>
            <ul className="space-y-4">
              <li><a href="#" className="text-gray-600 hover:text-finance-teal transition-colors duration-200">About</a></li>
              <li><a href="#" className="text-gray-600 hover:text-finance-teal transition-colors duration-200">Careers</a></li>
              <li><a href="#" className="text-gray-600 hover:text-finance-teal transition-colors duration-200">Press</a></li>
              <li><a href="#" className="text-gray-600 hover:text-finance-teal transition-colors duration-200">Contact</a></li>
            </ul>
          </div>
        </div>
        
        <div className="pt-8 border-t border-gray-200">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-500 text-sm">
              © {new Date().getFullYear()} AuditAI. All rights reserved.
            </p>
            <div className="flex space-x-6 mt-4 md:mt-0">
              <a href="#" className="text-gray-500 hover:text-finance-teal text-sm transition-colors duration-200">Privacy Policy</a>
              <a href="#" className="text-gray-500 hover:text-finance-teal text-sm transition-colors duration-200">Terms of Service</a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
