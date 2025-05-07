
import { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Menu } from "lucide-react";

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white shadow-sm">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <a href="#" className="flex items-center">
              <span className="text-xl font-bold text-finance-navy">Audit<span className="text-finance-teal">AI</span></span>
            </a>
          </div>
          
          <div className="hidden md:flex items-center space-x-8">
            <a href="#features" className="text-gray-600 hover:text-finance-teal transition-colors duration-200">Features</a>
            <a href="#how-it-works" className="text-gray-600 hover:text-finance-teal transition-colors duration-200">How it Works</a>
            <a href="#testimonials" className="text-gray-600 hover:text-finance-teal transition-colors duration-200">Testimonials</a>
            <Button className="btn-primary">Get Started</Button>
          </div>
          
          <div className="md:hidden">
            <Button variant="ghost" size="icon" onClick={() => setIsMenuOpen(!isMenuOpen)}>
              <Menu className="h-6 w-6" />
            </Button>
          </div>
        </div>
      </div>
      
      {isMenuOpen && (
        <div className="md:hidden bg-white py-2">
          <div className="container mx-auto px-4 space-y-2">
            <a href="#features" className="block py-2 text-gray-600 hover:text-finance-teal transition-colors duration-200">Features</a>
            <a href="#how-it-works" className="block py-2 text-gray-600 hover:text-finance-teal transition-colors duration-200">How it Works</a>
            <a href="#testimonials" className="block py-2 text-gray-600 hover:text-finance-teal transition-colors duration-200">Testimonials</a>
            <Button className="btn-primary w-full mt-2">Get Started</Button>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
