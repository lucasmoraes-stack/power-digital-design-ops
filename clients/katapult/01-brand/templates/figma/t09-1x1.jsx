const imgPhotoCard = "assets/77d7cc10-b398-4ed1-b8bc-5c9522217c84.png";
const imgKatapultLogoWhite = "assets/8d0e15c0-2a6b-41d0-8ff9-2fda8a5cc318.svg";

export default function Template09HeroPhotoFullWidth() {
  return (
    <div className="bg-[#131540] relative size-full" data-node-id="547:1164" data-name="template-09-hero-photo-full-width">
      <div className="absolute h-[685px] left-0 rounded-[8px] top-[515px] w-[1200px]" data-node-id="547:1165" data-name="photo-card">
        <div aria-hidden className="absolute inset-0 pointer-events-none rounded-[8px]">
          <div className="absolute inset-0 overflow-hidden rounded-[8px]">
            <img alt="" className="absolute h-[203.04%] left-0 max-w-none top-[-49.18%] w-full" src={imgPhotoCard} />
          </div>
          <div className="absolute bg-[rgba(0,0,0,0.25)] inset-0 rounded-[8px]" />
        </div>
      </div>
      <p className="-translate-x-1/2 [text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] absolute font-['Inter:Medium'] font-medium leading-[1.2] left-[calc(87.5%-146.5px)] not-italic text-[15px] text-center text-white top-[1085px] w-[489px]" data-node-id="547:1166">
        Lease-purchase service. Total cost exceeds cash price. Approval required. Not available in MN, NJ, WI, WY. See katapult.com.
      </p>
      <div className="absolute content-stretch flex flex-col gap-[59px] items-start left-[64px] top-[87px] w-[998px]" data-node-id="547:1167">
        <div className="content-stretch flex items-center relative shrink-0" data-node-id="547:1168">
          <div className="h-[31.616px] relative shrink-0 w-[142px]" data-node-id="547:1169" data-name="Katapult Logo (White)">
            <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgKatapultLogoWhite} />
          </div>
        </div>
        <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[0] not-italic relative shrink-0 text-[108.059px] text-white tracking-[-4.3224px] w-[815.353px]" data-node-id="547:1175">
          <span className="leading-[0.9]">{`Your next upgrade `}</span>
          <span className="leading-[0.9] text-[#ed5370]">awaits.</span>
        </p>
        <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.3] min-w-full not-italic relative shrink-0 text-[36px] text-[rgba(255,255,255,0.85)] w-[min-content]" data-node-id="547:1176">{`No credit required. Just the upgrade you've been wanting.`}</p>
      </div>
      <div className="absolute bg-[#ed5370] content-stretch flex items-center justify-center left-[64px] overflow-clip px-[64px] py-[32px] rounded-[49.5px] top-[1053px]" data-node-id="547:1177" data-name="Button">
        <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.2] not-italic relative shrink-0 text-[73.91px] text-white whitespace-nowrap" data-node-id="I547:1177;2485:67">
          Leap Forward
        </p>
      </div>
    </div>
  );
}