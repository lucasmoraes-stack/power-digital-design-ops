const imgPhotoCard = "assets/9a724f13-ae80-4b1f-99ba-0154444fd5c4.png";
const imgKatapultLogoWhite = "assets/55a9c427-d004-48a5-b593-664e035e0650.svg";

export default function Template09HeroPhotoFullWidth4X5() {
  return (
    <div className="bg-[#131540] relative size-full" data-node-id="547:1565" data-name="template-09-hero-photo-full-width-4x5">
      <div className="absolute h-[831.384px] left-0 rounded-[8px] top-[518.62px] w-[1080px]" data-node-id="547:1566" data-name="photo-card">
        <div aria-hidden className="absolute inset-0 pointer-events-none rounded-[8px]">
          <img alt="" className="absolute max-w-none object-cover rounded-[8px] size-full" src={imgPhotoCard} />
          <div className="absolute bg-[rgba(0,0,0,0.25)] inset-0 rounded-[8px]" />
        </div>
      </div>
      <p className="-translate-x-1/2 [text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] absolute font-['Inter:Medium'] font-medium leading-[1.2] left-[calc(75%-39.5px)] not-italic text-[15px] text-center text-white top-[1240px] w-[489px]" data-node-id="547:1567">
        Lease-purchase service. Total cost exceeds cash price. Approval required. Not available in MN, NJ, WI, WY. See katapult.com.
      </p>
      <div className="absolute content-stretch flex flex-col gap-[59px] items-start left-[65px] top-[80px] w-[950px]" data-node-id="547:1568">
        <div className="content-stretch flex items-center relative shrink-0" data-node-id="547:1569">
          <div className="h-[31.616px] relative shrink-0 w-[142px]" data-node-id="547:1570" data-name="Katapult Logo (White)">
            <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgKatapultLogoWhite} />
          </div>
        </div>
        <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[0] not-italic relative shrink-0 text-[108.059px] text-white tracking-[-4.3224px] w-[950px]" data-node-id="547:1576">
          <span className="leading-[0.9]">{`Your next upgrade `}</span>
          <span className="leading-[0.9] text-[#ed5370]">awaits.</span>
        </p>
        <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.3] not-italic relative shrink-0 text-[36px] text-[rgba(255,255,255,0.85)] w-[950px]" data-node-id="547:1577">{`No credit required. Just the upgrade you've been wanting.`}</p>
      </div>
      <div className="absolute bg-[#ed5370] content-stretch flex items-center justify-center left-[65px] overflow-clip px-[64px] py-[32px] rounded-[49.5px] top-[1205px]" data-node-id="547:1578" data-name="Button">
        <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.2] not-italic relative shrink-0 text-[73.91px] text-white whitespace-nowrap" data-node-id="I547:1578;2485:67">
          Leap Forward
        </p>
      </div>
    </div>
  );
}