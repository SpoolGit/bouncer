
import { Card, CardContent } from "@/components/ui/card";

const Testimonials = () => {
  const testimonials = [
    {
      quote: "AuditAI helped us reduce our audit time by 60% while increasing the accuracy of our findings. It's been a game-changer for our financial department.",
      name: "Sarah Johnson",
      title: "CFO, TechCorp Inc.",
      image: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=120&q=80"
    },
    {
      quote: "The AI-powered risk assessment has transformed how we approach financial auditing. We're now able to proactively address issues before they become problems.",
      name: "Michael Chen",
      title: "Head of Finance, Global Solutions",
      image: "https://images.unsplash.com/photo-1560250097-0b93528c311a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=120&q=80"
    },
    {
      quote: "The regulatory compliance features alone have saved us countless hours and potential fines. I can't imagine going back to our old auditing process.",
      name: "Alisha Patel",
      title: "Compliance Director, Finance Plus",
      image: "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=120&q=80"
    }
  ];

  return (
    <section id="testimonials" className="py-16 md:py-24 bg-finance-gray">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto text-center mb-12 md:mb-20">
          <span className="bg-finance-teal/10 text-finance-teal font-medium px-4 py-2 rounded-full text-sm mb-4 inline-block">Testimonials</span>
          <h2 className="text-3xl md:text-4xl font-bold text-finance-navy mb-6">
            Trusted by Financial Leaders
          </h2>
          <p className="text-xl text-gray-600">
            Hear what our clients have to say about their experience with AuditAI.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => (
            <Card key={index} className="border-0 shadow-lg">
              <CardContent className="p-8">
                <div className="flex flex-col h-full">
                  <div className="mb-6">
                    <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M9.33333 21.3333C7.86667 21.3333 6.66667 20.8 5.73333 19.7333C4.86667 18.6667 4.43333 17.3333 4.43333 15.7333C4.43333 14.2 4.83333 12.7333 5.63333 11.3333C6.5 9.86667 7.63333 8.66667 9.03333 7.73333L10.6667 9.33333C10.1333 9.73333 9.6 10.2667 9.06667 10.9333C8.53333 11.6 8.26667 12.1333 8.26667 12.5333C8.26667 12.9333 8.33333 13.2667 8.46667 13.5333C8.6 13.8 8.9 14 9.36667 14.1333C10.1333 14.3333 10.7333 14.7333 11.1667 15.3333C11.6 15.8667 11.8333 16.5333 11.8333 17.3333C11.8333 18.2667 11.5 19.0667 10.8333 19.7333C10.1667 20.8 9.33333 21.3333 9.33333 21.3333ZM21.3333 21.3333C19.8667 21.3333 18.6667 20.8 17.7333 19.7333C16.8667 18.6667 16.4333 17.3333 16.4333 15.7333C16.4333 14.2 16.8333 12.7333 17.6333 11.3333C18.5 9.86667 19.6333 8.66667 21.0333 7.73333L22.6667 9.33333C22.1333 9.73333 21.6 10.2667 21.0667 10.9333C20.5333 11.6 20.2667 12.1333 20.2667 12.5333C20.2667 12.9333 20.3333 13.2667 20.4667 13.5333C20.6 13.8 20.9 14 21.3667 14.1333C22.1333 14.3333 22.7333 14.7333 23.1667 15.3333C23.6 15.8667 23.8333 16.5333 23.8333 17.3333C23.8333 18.2667 23.5 19.0667 22.8333 19.7333C22.1667 20.8 21.3333 21.3333 21.3333 21.3333Z" fill="#0EA5E9"/>
                    </svg>
                  </div>
                  
                  <p className="text-gray-700 mb-8 flex-grow">
                    {testimonial.quote}
                  </p>
                  
                  <div className="flex items-center">
                    <div className="h-12 w-12 rounded-full overflow-hidden mr-4">
                      <img 
                        src={testimonial.image} 
                        alt={testimonial.name} 
                        className="h-full w-full object-cover"
                      />
                    </div>
                    <div>
                      <h4 className="font-semibold text-finance-navy">{testimonial.name}</h4>
                      <p className="text-sm text-gray-500">{testimonial.title}</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Testimonials;
