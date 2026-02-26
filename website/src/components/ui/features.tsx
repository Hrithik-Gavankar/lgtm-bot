import {
  Zap,
  Cpu,
  Fingerprint,
  Pencil,
  Settings2,
  Sparkles,
} from "lucide-react";

export function Features() {
  return (
    <section id="features" className="py-16 md:py-24 lg:py-27">
      <div className="mx-auto max-w-7xl space-y-12 px-6 md:space-y-11 lg:px-8">
        <div className="relative z-10 mx-auto max-w-4xl space-y-6 text-center md:space-y-8">
          <h2 className="text-balance text-4xl font-medium lg:text-3xl xl:text-3xl leading-tight">
            The foundation for automated code review and PR management
          </h2>
        </div>
        
        <div className="relative mx-auto grid max-w-7xl sm:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8">
          <div className="group space-y-5 p-8 lg:p-10 bg-white/[0.03] hover:bg-white/[0.06] backdrop-blur-sm rounded-3xl transition-all duration-300 border border-white/[0.05] hover:border-white/10">
            <div className="flex items-center gap-4">
              <div className="p-3 rounded-xl bg-white/5 group-hover:bg-white/10 transition-colors">
                <Zap className="size-6 lg:size-7" />
              </div>
              <h3 className="text-lg lg:text-xl font-semibold">AI-Powered Reviews</h3>
            </div>
            <p className="text-base lg:text-lg text-white/50 leading-relaxed">
              Analyze pull requests automatically for code quality, test
              coverage, and security using GPT, Claude, and local LLMs.
            </p>
          </div>
          
          <div className="group space-y-5 p-8 lg:p-10 bg-white/[0.03] hover:bg-white/[0.06] backdrop-blur-sm rounded-3xl transition-all duration-300 border border-white/[0.05] hover:border-white/10">
            <div className="flex items-center gap-4">
              <div className="p-3 rounded-xl bg-white/5 group-hover:bg-white/10 transition-colors">
                <Cpu className="size-6 lg:size-7" />
              </div>
              <h3 className="text-lg lg:text-xl font-semibold">Jira Integration</h3>
            </div>
            <p className="text-base lg:text-lg text-white/50 leading-relaxed">
              Extract problem description and acceptance criteria directly from
              Jira tickets for precise and context-aware reviews.
            </p>
          </div>
          
          <div className="group space-y-5 p-8 lg:p-10 bg-white/[0.03] hover:bg-white/[0.06] backdrop-blur-sm rounded-3xl transition-all duration-300 border border-white/[0.05] hover:border-white/10">
            <div className="flex items-center gap-4">
              <div className="p-3 rounded-xl bg-white/5 group-hover:bg-white/10 transition-colors">
                <Fingerprint className="size-6 lg:size-7" />
              </div>
              <h3 className="text-lg lg:text-xl font-semibold">Objective Scoring</h3>
            </div>
            <p className="text-base lg:text-lg text-white/50 leading-relaxed">
              Generates pass/fail scores with detailed explanations to help you
              understand review results clearly.
            </p>
          </div>
          
          <div className="group space-y-5 p-8 lg:p-10 bg-white/[0.03] hover:bg-white/[0.06] backdrop-blur-sm rounded-3xl transition-all duration-300 border border-white/[0.05] hover:border-white/10">
            <div className="flex items-center gap-4">
              <div className="p-3 rounded-xl bg-white/5 group-hover:bg-white/10 transition-colors">
                <Pencil className="size-6 lg:size-7" />
              </div>
              <h3 className="text-lg lg:text-xl font-semibold">Configurable</h3>
            </div>
            <p className="text-base lg:text-lg text-white/50 leading-relaxed">
              Customize review criteria, fail keywords, and output formats to
              fit your team&apos;s workflow.
            </p>
          </div>
          
          <div className="group space-y-5 p-8 lg:p-10 bg-white/[0.03] hover:bg-white/[0.06] backdrop-blur-sm rounded-3xl transition-all duration-300 border border-white/[0.05] hover:border-white/10">
            <div className="flex items-center gap-4">
              <div className="p-3 rounded-xl bg-white/5 group-hover:bg-white/10 transition-colors">
                <Settings2 className="size-6 lg:size-7" />
              </div>
              <h3 className="text-lg lg:text-xl font-semibold">Multi-Model Support</h3>
            </div>
            <p className="text-base lg:text-lg text-white/50 leading-relaxed">
              Supports OpenAI, Anthropic, and Ollama with options for cloud or
              local inference.
            </p>
          </div>
          
          <div className="group space-y-5 p-8 lg:p-10 bg-white/[0.03] hover:bg-white/[0.06] backdrop-blur-sm rounded-3xl transition-all duration-300 border border-white/[0.05] hover:border-white/10">
            <div className="flex items-center gap-4">
              <div className="p-3 rounded-xl bg-white/5 group-hover:bg-white/10 transition-colors">
                <Sparkles className="size-6 lg:size-7" />
              </div>
              <h3 className="text-lg lg:text-xl font-semibold">CI/CD Ready</h3>
            </div>
            <p className="text-base lg:text-lg text-white/50 leading-relaxed">
              Integrate easily with GitHub Actions for seamless automated code
              review in your development pipeline.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}