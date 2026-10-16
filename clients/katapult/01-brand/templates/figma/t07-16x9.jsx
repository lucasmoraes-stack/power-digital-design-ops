const imgAdobeStock4022200351 = "assets/2572a207-6f28-4bee-a138-0488d4c5be2c.png";
const imgSoftCircleBg = "assets/5932590b-6fad-445a-97ec-c614004e0848.svg";
const imgKatapultLogoWhite = "assets/33806527-be10-4849-9dca-13601712b3fa.svg";

export default function Template07TopBlockRoundedCard16X9() {
  return (
    <div className="bg-[#ed5370] relative size-full" data-node-id="547:1493" data-name="template-07-top-block-rounded-card-16x9">
      <div className="absolute left-[calc(50%+228.97px)] size-[566.06px] top-[256.97px]" data-node-id="547:1494" data-name="soft-circle-bg">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgSoftCircleBg} />
      </div>
      <div className="-translate-x-1/2 absolute content-stretch flex flex-col gap-[48px] items-center left-[calc(25%+40px)] top-[290.69px]" data-node-id="547:1495">
        <div className="content-stretch flex items-center relative shrink-0" data-node-id="547:1496">
          <div className="h-[31.616px] relative shrink-0 w-[142px]" data-node-id="547:1497" data-name="Katapult Logo (White)">
            <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgKatapultLogoWhite} />
          </div>
        </div>
        <div className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[0] not-italic relative shrink-0 text-[120px] text-center text-white tracking-[-4.8px] w-[960px]" data-node-id="547:1503">
          <p className="leading-[0.9] mb-0">Your upgrade</p>
          <p className="leading-[0.9]">starts here.</p>
        </div>
        <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.3] not-italic relative shrink-0 text-[40px] text-[rgba(255,255,255,0.85)] whitespace-nowrap" data-node-id="547:1504">
          No credit score needed. Just tap and say yes.
        </p>
        <div className="bg-[#131540] content-stretch flex items-center justify-center overflow-clip px-[64px] py-[32px] relative rounded-[49.5px] shrink-0" data-node-id="547:1505" data-name="Button">
          <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.2] not-italic relative shrink-0 text-[73.91px] text-white whitespace-nowrap" data-node-id="I547:1505;2485:67">
            Leap Forward
          </p>
        </div>
      </div>
      <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] absolute font-['Inter:Medium'] font-medium leading-[1.2] left-[calc(50%-405.5px)] not-italic text-[15px] text-white top-[1027px] w-[811px]" data-node-id="547:1506">
        Lease-purchase service. Total cost exceeds cash price. Approval required. Not available in MN, NJ, WI, WY. See katapult.com.
      </p>
      <div className="-translate-x-1/2 absolute h-[301.94px] left-[calc(87.5%-208.31px)] top-[279.29px] w-[450.12px]" data-node-id="547:1507" data-name="AdobeStock_402220035 1">
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <img alt="" className="absolute h-[161.26%] left-[-12.59%] max-w-none top-[-30.59%] w-[125.08%]" src={imgAdobeStock4022200351} />
        </div>
      </div>
    </div>
  );
}